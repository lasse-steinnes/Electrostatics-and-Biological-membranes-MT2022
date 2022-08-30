"""
Program to validate the iterative method, using a constructed electrostatic potential
"""

import numpy as np
#from mpi4py import MPI
#import pmesh.pm as pmesh
import matplotlib.pyplot as plt
from scipy import special

### Setting up the potential ###
def psi_analytic(x,y,z,mu_x,mu_y,mu_z):
    sigma = 0.5
    d = 3
    denom = ((sigma**d) * (np.sqrt(2 * np.pi)**d))
    A = 1.0/denom
    return A * np.exp(-(1/(2 * sigma**2)) * ((x - mu_x)**2 + (y - mu_y)**2 \
            + (z - mu_z)**2)) # + (z - mu_z)**2))
"""
At least now it has the correct shape with d = 1
"""

x = np.linspace(-5,5,1000, dtype = float)
y = np.linspace(-5,5,1000, dtype = float)
z = np.linspace(-5,5,1000,dtype = float)
mu_x = mu_y = mu_z = 0.0

### Setting up the dielectric permittivity ###
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
    c = 2.0/np.sqrt(np.pi)*(eps_0 - 1)
    expr1 = eps(x,y,z)*(r**2/sigma**4 - 3.0/sigma**2)*f(x,y,z,mu_x,mu_y,mu_z)
    expr2 = r/(delta*sigma**2)*f(x,y,z,mu_x,mu_y,mu_z)*np.exp(-((r-d0)/delta)**2)
    return -1.0*(expr1 - c*expr2)


### Get the densities with numpy gradient ###
grad_psi = np.gradient(psi_analytic(x,y,z,mu_x,mu_y,mu_z))
densities = -np.gradient(dielectric(x,y,z)*grad_psi)


# create figure and axis objects with subplots()
fig,ax = plt.subplots(figsize = (8,6))
l1 ,= ax.plot(x, psi_analytic(x,y,z,mu_x,mu_y,mu_z), color = "grey")
l3 ,= ax.plot(x,densities_analytic(x,y,z,mu_x,mu_y,mu_z)*(1/(4*np.pi)),"--" ,color = "grey")
#l3 ,= ax.plot(x,densities*800,"--" ,color = "grey")
ax.set_xlabel("x [arbritary units]",fontsize = 14)
ax.set_ylabel(r"$\psi(\mathbf{r})$", color = "grey", fontsize=14)
ax2=ax.twinx()
l2 ,= ax2.plot(x,dielectric(x,y,z), color = "black")
ax2.set_ylabel(r"$\varepsilon(\mathbf{r})$", fontsize = 14)
plt.legend([l1, l2,l3],[ r"$\psi(\mathbf{r})$",r"$\varepsilon(\mathbf{r})$",r"$\rho(\mathbf{r})\cdot 1/4\pi$ (Gaussian units)"], loc = "center right")
plt.tight_layout()
#plt.ylim([-0])
plt.show()

### Now using pmesh to construct meshes ###
#print(np.shape(densities))
print(np.shape(grad_psi))
### Validate the code ###
