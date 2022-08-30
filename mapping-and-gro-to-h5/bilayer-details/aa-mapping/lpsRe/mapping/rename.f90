program topbuilder

  integer :: i, j, k, l, m, ierr

  character :: atom*6, nameatom*4, resname*5, space*4
  character :: a11*10, a12*6, a13*3, a14*5
  character :: a21*10, a22*5, a23*3, a24*2, a25*11, a26*3
  character :: a31*8, a32*9, a33*9, a34*7, a35*7, a36*7, a37*7, a38*2, a39*14
  character :: a41*5, a42*9
  character :: a5*3, a6*6, aux*14

  integer :: numatom, numres

  real :: x, y, z
  
  open(1, file='mapped-traj.pdb', status='old')
  open(2, file='correct.pdb', status='new')
  
100 format (a6,i5,a6,a5,i4,a4,3f8.3,a14)

  i = 1
  ierr = 0
  
  do while (i<=5001)

     read(1,'(a10,a6,a3,a5)',IOSTAT=ierr) a11, a12, a13, a14
     write(2,'(a10,a6,a3,a5)') a11, a12, a13, a14

     read(1,'(a10,a5,a3,a2,a11,a3)') a21,a22,a23,a24,a25,a26
     write(2,'(a10,a5,a3,a2,a11,a3)') a21,a22,a23,a24,a25,a26

     read(1,'(a8,a9,a9,a7,a7,a7,a7,a2,a14)') a31,a32,a33,a34,a35,a36,a37,a38,a39
     write(2,'(a8,a9,a9,a7,a7,a7,a7,a2,a14)') a31,a32,a33,a34,a35,a36,a37,a38,a39

     read(1,'(a5,a9)') a41,a42
     write(2,'(a5,a9)') a41,a42
     
     j = 1

     do while ( j <= 256 )

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   P1  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   P2  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   G1  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   G2  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   G3  ", 'LRe', j, space, x, y, z, aux
        
        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   L1  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   C1  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   C2  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   C3  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
	write(2,100) atom, numatom, "   G4  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   C4  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   C5  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   C6  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   C7  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   C8  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   L2  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
	write(2,100) atom, numatom, "   G5  ", 'LRe', j, space, x, y, z, aux
 
        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   L3  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   G6  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   C9  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "  C10  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "  C11  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "  C12  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "  C13  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "  C14  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
	write(2,100) atom, numatom, "   P3  ", 'LRe', j, space, x, y, z, aux
        
        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   L4  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   L5  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   L6  ", 'LRe', j, space, x, y, z, aux
        
        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
	write(2,100) atom, numatom, "   P4  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   L7  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   L8  ", 'LRe', j, space, x, y, z, aux

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   L9  ", 'LRe', j, space, x, y, z, aux
 
        j = j + 1

     END do

     do while ( j <= 768 )

        read(1,100,IOSTAT=ierr) atom, numatom, nameatom, resname, numres, space, x, y, z, aux
        write(2,100) atom, numatom, "   N   ", ' N ', j, space, x, y, z, aux
        
        j = j + 1
        
     end do

99   format (a6,i5,a5,a5,i5,a4,3f8.3,a14)
     
     do while ( j <= 12647 )

        read(1,99,IOSTAT=ierr) atom, numatom, resname, resname, numres, space, x, y, z, aux
        write(2,99) atom, numatom, "   W  ", 'SOL', j, space, x, y, z, aux

        j = j + 1
        
     end do
     
     read(1,'(a3)') a5
     write(2,'(a3)') a5

     read(1,'(a6)') a6
     write(2,'(a6)') a6

     write(*,*) i
     i = i + 1
     
  end do

  close(1)
  close(2)

end program topbuilder
