# Programme to create heat maps to decice on the smoothing parameter
import numpy as np
from mpi4py import MPI
import pmesh.pm as pmesh
import matplotlib.pyplot as plt
from scipy import special # error func

comm = MPI.COMM_WORLD

## setting up the needed functions
def psi_analytic(x,y,z,mu_x,mu_y,mu_z):
    sigma = 0.5
    d = 3
    denom = ((sigma**d) * (np.sqrt(2 * np.pi)**d))
    A = 1.0/denom
    return A * np.exp(-(1/(2 * sigma**2)) * ((x - mu_x)**2 + (y - mu_y)**2 \
            + (z - mu_z)**2))

def dielectric(x,y,z):
    eps_0 = 78.36; delta = 0.3; d0 = 1.7
    r = np.sqrt(x**2 + y**2 + z**2) # + z**2) #+ z**2)
    h = 1.0/2 * (1 + special.erf((r - d0)/delta))
    return 1 + (eps_0 - 1) * h


def densities_analytic(x,y,z,mu_x,mu_y,mu_z, eps = dielectric, f = psi_analytic):
    d = 3
    eps_0 = 78.36; delta = 0.3; d0 = 1.7
    r = np.sqrt(x**2 + y**2 + z**2)
    sigma = 0.5
    ## gromacs units
    COULK_GMX = 138.935458 # the 1/(4pi eps0) Gromacs units  ## need to use pmesh units, then transfer back
    eps_vacuum = 1.0/(COULK_GMX*4*np.pi)
    c = 1.0/np.sqrt(np.pi)*(eps_0 - 1)
    expr1 = eps(x,y,z)*(r**2/sigma**4 - 3.0/sigma**2)*f(x,y,z,mu_x,mu_y,mu_z)
    expr2 = r/(delta*sigma**2)*f(x,y,z,mu_x,mu_y,mu_z)*np.exp(-((r-d0)/delta)**2)
    return -1.0*(expr1 - c*expr2)*eps_vacuum


# spatial arrays
N = 32
x = np.linspace(-5,5,N, dtype = "f4")
y = np.linspace(-5,5,N, dtype = "f4")
z = np.linspace(-5,5,N,dtype = "f4")
mu_x = mu_y = mu_z = 0.0

#plt.plot(x,densities_eps_const(x,y,z,mu_x,mu_y,mu_z,))
#plt.show()

dims = 3
X, Y, Z = np.meshgrid(x,y,z, indexing = "ij")


e_r = dielectric(X,Y,Z)
rho_q = densities_analytic(X,Y,Z,mu_x,mu_y,mu_z)
psi_ana = psi_analytic(X,Y,Z,mu_x,mu_y,mu_z)


### Preprocessing with pmesh
# The first argument of ParticleMesh has to be a tuple
box_size = [10.0, 10.0, 10.0]
mesh_size = [N,N,N]


pm = pmesh.ParticleMesh(mesh_size, BoxSize=box_size, dtype="f4") ## comm == comm omitted
# using 64 bit to validate

phi_q = pm.create("real", value=0.0)
phi_q_fourier = pm.create("complex", value=0.0)

## GPE relevant
phi_q_eps = pm.create("real", value = 0.0) ## real contrib of non-polarization part of GPE
phi_q_eps_fourier = pm.create("complex", value = 0.0) # complex contrib of phi q eps
phi_q_effective_fourier = pm.create("complex", value = 0.0) ## fourier of non-polarization part of GPE
phi_eps = pm.create("real", value = 0.0) ## real contrib of the epsilon dielectric painted to grid
phi_eps_fourier = pm.create("complex", value = 0.0) # complex contrib of phi eps
phi_eta = [pm.create("real", value = 0.0)for _ in range(dims)] ## real contrib of factor in polarization charge density
phi_eta_fourier = [pm.create("complex", value = 0.0)for _ in range(dims)] ## fourier of factor in polarization charge density
phi_pol = pm.create("real", value = 0.0) ## real contrib of the polarization charge
phi_pol_fourier = [pm.create("complex", value = 0.0) for _ in range(dims)] # complex contrib of the polarization charge
phi_pol_temp = [pm.create("real", value = 0.0) for _ in range (dims)] # complex contrib of the polarization charge
sum_fourier = pm.create("complex", value = 0.0)

## fill in values for phi_q, still keeping it a pmesh object
for i in range(N):
    for j in range(N):
        for k in range(N):
            phi_q[i,j,k] = rho_q[i,j,k]

## fill in for epsilon
for i in range(N):
    for j in range(N):
        for k in range(N):
            phi_eps[i,j,k] = e_r[i,j,k]

## basic setup
phi_q.r2c(out=phi_q_fourier)

#### With filtering
sigma_filter = 0.9 # filter off if zero
def phi_transfer_function(k, v):
        return v * np.exp(-0.5*sigma_filter**2*k.normp(p=2, zeromode=1))

phi_q_fourier.apply(phi_transfer_function, out=phi_q_fourier)
## ^------ use the same gaussian as the \kai interaciton
## ^------ tbr; phi_transfer_funciton by hamiltonian.H ??
phi_q_fourier.c2r(out=phi_q) ## this phi_q is after applying the smearing function


phi_q_eps = (phi_q/phi_eps)
phi_q_eps.r2c(out = phi_q_eps_fourier)
phi_eps.r2c(out=phi_eps_fourier)
##^ Get effective charge densities

_SPACE_DIM = 3


COULK_GMX = 138.935458 # the 1/(4pi eps0) Gromacs units  ## need to use pmesh units, then transfer back
eps_0 = 1.0/(COULK_GMX*4*np.pi)
##^--------- constants needed throughout the calculations

### method for finding the gradient (fourier space), using the spatial dimension of k
for _d in np.arange(_SPACE_DIM):
    def gradient_transfer_function(k,x, d =_d):
        return  1j*k[_d]*x

    phi_eps_fourier.apply(gradient_transfer_function, out = phi_eta_fourier[_d])
    phi_eta_fourier[_d].c2r(out = phi_eta[_d])
    phi_eta[_d] = phi_eta[_d]/phi_eps # the eta param used in the iterative method

#def conv_fun(comm,diffmesh):
#    return diffmesh.cnorm()

#def conv_func(comm,diffmesh):
#    return diffmesh.csum()

def conv_fun(comm,diffmesh):
    msg = np.max(diffmesh)
    res = comm.allreduce(sendobj=msg, op=MPI.MAX)
    return res

def iterate_apply_k_vec(k,additive_terms,d = _d):
    return additive_terms * (- 1j * k[_d]) / k.normp(p=2, zeromode=1)

max_iter = 200

dw = 0.05
end = 1.0
start = 0.2
n_points = int((end-start)/dw)
w = np.linspace(start,end, n_points+1)
accuracy = np.zeros((len(w),max_iter))

### make heatmap

### Needed for the electrostatic potential comparison
for j in range(len(w)):
    print("j: {:d} out of {:} ".format(j+1,len(w)))
    omega = w[j]

    def k_norm_divide(k, potential):
            return potential/k.normp(p=2, zeromode = 1)

    ## > Electrostatic potential
    eps0_inv = COULK_GMX*4*np.pi
    ## ^ the 1/(4pi eps0)*4*pi = 1/eps0
    elec_potential_fourier =  pm.create("complex", value = 0.0)
    elec_potential = pm.create("real", value = 0.0)

    ### iterative GPE solver ###
    ### ----------------------------------------------
    phi_pol = pm.create("real", value = 0.0) ## real contrib of the polarization charge
    phi_pol_prev = pm.create("real", value = 0.0)
    i = 0; delta = 1.0
    while (i < max_iter):
        (phi_q_eps + phi_pol_prev).r2c(out=sum_fourier)
        for _d in np.arange(_SPACE_DIM):
            sum_fourier.apply(iterate_apply_k_vec,out = phi_pol_fourier[_d])
            phi_pol_fourier[_d].c2r(out = phi_pol_temp[_d])

        phi_pol = -(phi_eta[0]*phi_pol_temp[0] + \
                     phi_eta[1]*phi_pol_temp[1] +  phi_eta[2]*phi_pol_temp[2]);
        ### ^-- Following a positive sign convention (ik) of the FT, pos sign
        ### --- mathematically correct by the definition of the GPE
        phi_pol = omega*phi_pol + (1.0-omega)*phi_pol_prev
        phi_pol_prev = phi_pol.copy() # best to work with copy?
        i = i + 1

        ### obtain accuracy
        ((eps0_inv)*(phi_q_eps + phi_pol)).r2c(out = elec_potential_fourier)
        elec_potential_fourier.apply(k_norm_divide, out = elec_potential_fourier)
        elec_potential_fourier.c2r(out = elec_potential)

        ## using the max difference
        accuracy[j,i-1] = np.max(np.abs(elec_potential - psi_ana))

bit_type = 4 # 32, optional 8 --> 64 bit

### Store data
f = open("./validation-map-iterations-{:d}-f{:d}-N{:d}-filter09.txt".format(max_iter,bit_type,N), "w")
for j in range(len(w)):
    for i in range(max_iter):
        f.write("{:.2e} ".format(accuracy[j,i]))
    f.write("\n")
f.close()
