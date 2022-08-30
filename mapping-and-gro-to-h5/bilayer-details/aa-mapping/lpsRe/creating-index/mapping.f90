program allmap

  use functions

  type(beads) :: p1, p2, p3, p4, g1, g2, g3, g4, g5, g6
  type(beads) :: l1, l2, l3, l4, l5, l6 ,l7, l8, l9
  type(beads) :: c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14
  
  character*6 :: aux
  
  integer :: i, ierr

  open(1, file='cgbuilder.ndx', status='old')

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) p1%a1, p1%a2, p1%a3, p1%a4, p1%a5, p1%a6

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) p2%a1, p2%a2, p2%a3, p2%a4, p2%a5, p2%a6

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) g1%a1, g1%a2, g1%a3, g1%a4

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) g2%a1, g2%a2, g2%a3, g2%a4

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) g3%a1, g3%a2, g3%a3, g3%a4, g3%a5, g3%a6

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) l1%a1, l1%a2, l1%a3, l1%a4, l1%a5

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c1%a1, c1%a2, c1%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c2%a1, c2%a2, c2%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c3%a1, c3%a2, c3%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) g4%a1, g4%a2, g4%a3, g4%a4, g4%a5

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c4%a1, c4%a2, c4%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c5%a1, c5%a2, c5%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c6%a1, c6%a2, c6%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c7%a1, c7%a2, c7%a3, c7%a4

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c8%a1, c8%a2, c8%a3, c8%a4
  
  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) l2%a1, l2%a2, l2%a3, l2%a4, l2%a5, l2%a6

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) g5%a1, g5%a2, g5%a3, g5%a4, g5%a5, g5%a6
  
  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) l3%a1, l3%a2, l3%a3, l3%a4

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) g6%a1, g6%a2, g6%a3, g6%a4, g6%a5

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c9%a1, c9%a2, c9%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c10%a1, c10%a2, c10%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c11%a1, c11%a2, c11%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c12%a1, c12%a2, c12%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c13%a1, c13%a2, c13%a3, c13%a4

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) c14%a1, c14%a2, c14%a3, c14%a4

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) p3%a1, p3%a2, p3%a3, p3%a4, p3%a5

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) l4%a1, l4%a2, l4%a3, l4%a4, l4%a5, l4%a6

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) l5%a1, l5%a2, l5%a3, l5%a4, l5%a5

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) l6%a1, l6%a2, l6%a3

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) p4%a1, p4%a2, p4%a3, p4%a4

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) l7%a1, l7%a2, l7%a3, l7%a4

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) l8%a1, l8%a2, l8%a3, l8%a4, l8%a5

  read(1, *, IOSTAT=ierr) aux

  read(1, *, IOSTAT=ierr) l9%a1, l9%a2, l9%a3, l9%a4, l9%a5, l9%a6
  
  close(1)
  
  open(3, file='new.ndx', status='new', iostat=ierr)
  
  i = 1

  do while ( i <= 9 )  
     
     write(3,'(a2,i1,a4)') '[ ',i,'P1 ]'
     write(3,*) p1%a1+141*(i-1), p1%a2+141*(i-1), p1%a3+141*(i-1), p1%a4+141*(i-1), p1%a5+141*(i-1), p1%a6+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a4)') '[ ',i,'P2 ]'
     write(3, *) p2%a1+141*(i-1), p2%a2+141*(i-1), p2%a3+141*(i-1), p2%a4+141*(i-1), p2%a5+141*(i-1), p2%a6+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a4)') '[ ',i,'G1 ]'
     write(3,*) g1%a1+141*(i-1), g1%a2+141*(i-1), g1%a3+141*(i-1), g1%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a4)') '[ ',i,'G2 ]'
     write(3,*) g2%a1+141*(i-1), g2%a2+141*(i-1), g2%a3+141*(i-1), g2%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a4)') '[ ',i,'G3 ]'
     write(3,*) g3%a1+141*(i-1), g3%a2+141*(i-1), g3%a3+141*(i-1), g3%a4+141*(i-1), g3%a5+141*(i-1), g3%a6+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'L1 ]'
     write(3,*) l1%a1+141*(i-1), l1%a2+141*(i-1), l1%a3+141*(i-1), l1%a4+141*(i-1), l1%a5+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'C1 ]'
     write(3,*) c1%a1+141*(i-1), c1%a2+141*(i-1), c1%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'C2 ]'
     write(3,*) c2%a1+141*(i-1), c2%a2+141*(i-1), c2%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'C3 ]'
     write(3,*) c3%a1+141*(i-1), c3%a2+141*(i-1), c3%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'G4 ]'
     write(3,*) g4%a1+141*(i-1), g4%a2+141*(i-1), g4%a3+141*(i-1), g4%a4+141*(i-1), g4%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a4)') '[ ',i,'C4 ]'
     write(3,*) c4%a1+141*(i-1), c4%a2+141*(i-1), c4%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'C5 ]'
     write(3,*) c5%a1+141*(i-1), c5%a2+141*(i-1), c5%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'C6 ]'
     write(3,*) c6%a1+141*(i-1), c6%a2+141*(i-1), c6%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'C7 ]'
     write(3,*) c7%a1+141*(i-1), c7%a2+141*(i-1), c7%a3+141*(i-1), c7%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'C8 ]'
     write(3,*) c8%a1+141*(i-1), c8%a2+141*(i-1), c8%a3+141*(i-1), c8%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'L2 ]'
     write(3,*) l2%a1+141*(i-1), l2%a2+141*(i-1), l2%a3+141*(i-1), l2%a4+141*(i-1), l2%a5+141*(i-1), l2%a6+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'G5 ]'
     write(3,*) g5%a1+141*(i-1), g5%a2+141*(i-1), g5%a3+141*(i-1), g5%a4+141*(i-1), g5%a5+141*(i-1), g5%a6+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a4)') '[ ',i,'L3 ]'
     write(3,*) l3%a1+141*(i-1), l3%a2+141*(i-1), l3%a3+141*(i-1), l3%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a4)') '[ ',i,'G6 ]'
     write(3,*) g6%a1+141*(i-1), g6%a2+141*(i-1), g6%a3+141*(i-1), g6%a4+141*(i-1), g6%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a4)') '[ ',i,'C9 ]'
     write(3,*) c9%a1+141*(i-1), c9%a2+141*(i-1), c9%a3+141*(i-1) 
     write(3,*)
     
     write(3,'(a2,i1,a5)') '[ ',i,'C10 ]'
     write(3,*) c10%a1+141*(i-1), c10%a2+141*(i-1), c10%a3+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a5)') '[ ',i,'C11 ]'
     write(3,*) c11%a1+141*(i-1), c11%a2+141*(i-1), c11%a3+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a5)') '[ ',i,'C12 ]'
     write(3,*) c12%a1+141*(i-1), c12%a2+141*(i-1), c12%a3+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a5)') '[ ',i,'C13 ]'
     write(3,*) c13%a1+141*(i-1), c13%a2+141*(i-1), c13%a3+141*(i-1), c13%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a5)') '[ ',i,'C14 ]'
     write(3,*) c14%a1+141*(i-1), c14%a2+141*(i-1), c14%a3+141*(i-1), c14%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'P3 ]'
     write(3, *) p3%a1+141*(i-1), p3%a2+141*(i-1), p3%a3+141*(i-1), p3%a4+141*(i-1), p3%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a4)') '[ ',i,'L4 ]'
     write(3,*) l4%a1+141*(i-1), l4%a2+141*(i-1), l4%a3+141*(i-1), l4%a4+141*(i-1), l4%a5+141*(i-1), l4%a6+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'L5 ]'
     write(3,*) l5%a1+141*(i-1), l5%a2+141*(i-1), l5%a3+141*(i-1), l5%a4+141*(i-1), l5%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i1,a4)') '[ ',i,'L6 ]'
     write(3,*) l6%a1+141*(i-1), l6%a2+141*(i-1), l6%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'P4 ]'
     write(3, *) p4%a1+141*(i-1), p4%a2+141*(i-1), p4%a3+141*(i-1), p4%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'L7 ]'
     write(3,*) l7%a1+141*(i-1), l7%a2+141*(i-1), l7%a3+141*(i-1), l7%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'L8 ]'
     write(3,*) l8%a1+141*(i-1), l8%a2+141*(i-1), l8%a3+141*(i-1), l8%a4+141*(i-1), l8%a5+141*(i-1)
     write(3,*)

     write(3,'(a2,i1,a4)') '[ ',i,'L9 ]'
     write(3,*) l9%a1+141*(i-1), l9%a2+141*(i-1), l9%a3+141*(i-1), l9%a4+141*(i-1), l9%a5+141*(i-1), l9%a6+141*(i-1)
     write(3,*)

     i = i + 1
     
  end do
  
  do while ( i <= 99 )  
     
     write(3,'(a2,i2,a4)') '[ ',i,'P1 ]'
     write(3,*) p1%a1+141*(i-1), p1%a2+141*(i-1), p1%a3+141*(i-1), p1%a4+141*(i-1), p1%a5+141*(i-1), p1%a6+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a4)') '[ ',i,'P2 ]'
     write(3, *) p2%a1+141*(i-1), p2%a2+141*(i-1), p2%a3+141*(i-1), p2%a4+141*(i-1), p2%a5+141*(i-1), p2%a6+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a4)') '[ ',i,'G1 ]'
     write(3,*) g1%a1+141*(i-1), g1%a2+141*(i-1), g1%a3+141*(i-1), g1%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a4)') '[ ',i,'G2 ]'
     write(3,*) g2%a1+141*(i-1), g2%a2+141*(i-1), g2%a3+141*(i-1), g2%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a4)') '[ ',i,'G3 ]'
     write(3,*) g3%a1+141*(i-1), g3%a2+141*(i-1), g3%a3+141*(i-1), g3%a4+141*(i-1), g3%a5+141*(i-1), g3%a6+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'L1 ]'
     write(3,*) l1%a1+141*(i-1), l1%a2+141*(i-1), l1%a3+141*(i-1), l1%a4+141*(i-1), l1%a5+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'C1 ]'
     write(3,*) c1%a1+141*(i-1), c1%a2+141*(i-1), c1%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'C2 ]'
     write(3,*) c2%a1+141*(i-1), c2%a2+141*(i-1), c2%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'C3 ]'
     write(3,*) c3%a1+141*(i-1), c3%a2+141*(i-1), c3%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'G4 ]'
     write(3,*) g4%a1+141*(i-1), g4%a2+141*(i-1), g4%a3+141*(i-1), g4%a4+141*(i-1), g4%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a4)') '[ ',i,'C4 ]'
     write(3,*) c4%a1+141*(i-1), c4%a2+141*(i-1), c4%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'C5 ]'
     write(3,*) c5%a1+141*(i-1), c5%a2+141*(i-1), c5%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'C6 ]'
     write(3,*) c6%a1+141*(i-1), c6%a2+141*(i-1), c6%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'C7 ]'
     write(3,*) c7%a1+141*(i-1), c7%a2+141*(i-1), c7%a3+141*(i-1), c7%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'C8 ]'
     write(3,*) c8%a1+141*(i-1), c8%a2+141*(i-1), c8%a3+141*(i-1), c8%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'L2 ]'
     write(3,*) l2%a1+141*(i-1), l2%a2+141*(i-1), l2%a3+141*(i-1), l2%a4+141*(i-1), l2%a5+141*(i-1), l2%a6+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'G5 ]'
     write(3,*) g5%a1+141*(i-1), g5%a2+141*(i-1), g5%a3+141*(i-1), g5%a4+141*(i-1), g5%a5+141*(i-1), g5%a6+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a4)') '[ ',i,'L3 ]'
     write(3,*) l3%a1+141*(i-1), l3%a2+141*(i-1), l3%a3+141*(i-1), l3%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a4)') '[ ',i,'G6 ]'
     write(3,*) g6%a1+141*(i-1), g6%a2+141*(i-1), g6%a3+141*(i-1), g6%a4+141*(i-1), g6%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a4)') '[ ',i,'C9 ]'
     write(3,*) c9%a1+141*(i-1), c9%a2+141*(i-1), c9%a3+141*(i-1) 
     write(3,*)
     
     write(3,'(a2,i2,a5)') '[ ',i,'C10 ]'
     write(3,*) c10%a1+141*(i-1), c10%a2+141*(i-1), c10%a3+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a5)') '[ ',i,'C11 ]'
     write(3,*) c11%a1+141*(i-1), c11%a2+141*(i-1), c11%a3+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a5)') '[ ',i,'C12 ]'
     write(3,*) c12%a1+141*(i-1), c12%a2+141*(i-1), c12%a3+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a5)') '[ ',i,'C13 ]'
     write(3,*) c13%a1+141*(i-1), c13%a2+141*(i-1), c13%a3+141*(i-1), c13%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a5)') '[ ',i,'C14 ]'
     write(3,*) c14%a1+141*(i-1), c14%a2+141*(i-1), c14%a3+141*(i-1), c14%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'P3 ]'
     write(3, *) p3%a1+141*(i-1), p3%a2+141*(i-1), p3%a3+141*(i-1), p3%a4+141*(i-1), p3%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a4)') '[ ',i,'L4 ]'
     write(3,*) l4%a1+141*(i-1), l4%a2+141*(i-1), l4%a3+141*(i-1), l4%a4+141*(i-1), l4%a5+141*(i-1), l4%a6+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'L5 ]'
     write(3,*) l5%a1+141*(i-1), l5%a2+141*(i-1), l5%a3+141*(i-1), l5%a4+141*(i-1), l5%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i2,a4)') '[ ',i,'L6 ]'
     write(3,*) l6%a1+141*(i-1), l6%a2+141*(i-1), l6%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'P4 ]'
     write(3, *) p4%a1+141*(i-1), p4%a2+141*(i-1), p4%a3+141*(i-1), p4%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'L7 ]'
     write(3,*) l7%a1+141*(i-1), l7%a2+141*(i-1), l7%a3+141*(i-1), l7%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'L8 ]'
     write(3,*) l8%a1+141*(i-1), l8%a2+141*(i-1), l8%a3+141*(i-1), l8%a4+141*(i-1), l8%a5+141*(i-1)
     write(3,*)

     write(3,'(a2,i2,a4)') '[ ',i,'L9 ]'
     write(3,*) l9%a1+141*(i-1), l9%a2+141*(i-1), l9%a3+141*(i-1), l9%a4+141*(i-1), l9%a5+141*(i-1), l9%a6+141*(i-1)
     write(3,*)
     
     i = i + 1
     
  end do

  do while ( i <= 128 )  
     
     write(3,'(a2,i3,a4)') '[ ',i,'P1 ]'
     write(3,*) p1%a1+141*(i-1), p1%a2+141*(i-1), p1%a3+141*(i-1), p1%a4+141*(i-1), p1%a5+141*(i-1), p1%a6+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i,'P2 ]'
     write(3, *) p2%a1+141*(i-1), p2%a2+141*(i-1), p2%a3+141*(i-1), p2%a4+141*(i-1), p2%a5+141*(i-1), p2%a6+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i,'G1 ]'
     write(3,*) g1%a1+141*(i-1), g1%a2+141*(i-1), g1%a3+141*(i-1), g1%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i,'G2 ]'
     write(3,*) g2%a1+141*(i-1), g2%a2+141*(i-1), g2%a3+141*(i-1), g2%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i,'G3 ]'
     write(3,*) g3%a1+141*(i-1), g3%a2+141*(i-1), g3%a3+141*(i-1), g3%a4+141*(i-1), g3%a5+141*(i-1), g3%a6+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'L1 ]'
     write(3,*) l1%a1+141*(i-1), l1%a2+141*(i-1), l1%a3+141*(i-1), l1%a4+141*(i-1), l1%a5+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'C1 ]'
     write(3,*) c1%a1+141*(i-1), c1%a2+141*(i-1), c1%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'C2 ]'
     write(3,*) c2%a1+141*(i-1), c2%a2+141*(i-1), c2%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'C3 ]'
     write(3,*) c3%a1+141*(i-1), c3%a2+141*(i-1), c3%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'G4 ]'
     write(3,*) g4%a1+141*(i-1), g4%a2+141*(i-1), g4%a3+141*(i-1), g4%a4+141*(i-1), g4%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i,'C4 ]'
     write(3,*) c4%a1+141*(i-1), c4%a2+141*(i-1), c4%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'C5 ]'
     write(3,*) c5%a1+141*(i-1), c5%a2+141*(i-1), c5%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'C6 ]'
     write(3,*) c6%a1+141*(i-1), c6%a2+141*(i-1), c6%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'C7 ]'
     write(3,*) c7%a1+141*(i-1), c7%a2+141*(i-1), c7%a3+141*(i-1), c7%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'C8 ]'
     write(3,*) c8%a1+141*(i-1), c8%a2+141*(i-1), c8%a3+141*(i-1), c8%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'L2 ]'
     write(3,*) l2%a1+141*(i-1), l2%a2+141*(i-1), l2%a3+141*(i-1), l2%a4+141*(i-1), l2%a5+141*(i-1), l2%a6+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'G5 ]'
     write(3,*) g5%a1+141*(i-1), g5%a2+141*(i-1), g5%a3+141*(i-1), g5%a4+141*(i-1), g5%a5+141*(i-1), g5%a6+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i,'L3 ]'
     write(3,*) l3%a1+141*(i-1), l3%a2+141*(i-1), l3%a3+141*(i-1), l3%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i,'G6 ]'
     write(3,*) g6%a1+141*(i-1), g6%a2+141*(i-1), g6%a3+141*(i-1), g6%a4+141*(i-1), g6%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i,'C9 ]'
     write(3,*) c9%a1+141*(i-1), c9%a2+141*(i-1), c9%a3+141*(i-1) 
     write(3,*)
     
     write(3,'(a2,i3,a5)') '[ ',i,'C10 ]'
     write(3,*) c10%a1+141*(i-1), c10%a2+141*(i-1), c10%a3+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a5)') '[ ',i,'C11 ]'
     write(3,*) c11%a1+141*(i-1), c11%a2+141*(i-1), c11%a3+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a5)') '[ ',i,'C12 ]'
     write(3,*) c12%a1+141*(i-1), c12%a2+141*(i-1), c12%a3+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a5)') '[ ',i,'C13 ]'
     write(3,*) c13%a1+141*(i-1), c13%a2+141*(i-1), c13%a3+141*(i-1), c13%a4+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a5)') '[ ',i,'C14 ]'
     write(3,*) c14%a1+141*(i-1), c14%a2+141*(i-1), c14%a3+141*(i-1), c14%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'P3 ]'
     write(3, *) p3%a1+141*(i-1), p3%a2+141*(i-1), p3%a3+141*(i-1), p3%a4+141*(i-1), p3%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i,'L4 ]'
     write(3,*) l4%a1+141*(i-1), l4%a2+141*(i-1), l4%a3+141*(i-1), l4%a4+141*(i-1), l4%a5+141*(i-1), l4%a6+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'L5 ]'
     write(3,*) l5%a1+141*(i-1), l5%a2+141*(i-1), l5%a3+141*(i-1), l5%a4+141*(i-1), l5%a5+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i,'L6 ]'
     write(3,*) l6%a1+141*(i-1), l6%a2+141*(i-1), l6%a3+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'P4 ]'
     write(3, *) p4%a1+141*(i-1), p4%a2+141*(i-1), p4%a3+141*(i-1), p4%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'L7 ]'
     write(3,*) l7%a1+141*(i-1), l7%a2+141*(i-1), l7%a3+141*(i-1), l7%a4+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'L8 ]'
     write(3,*) l8%a1+141*(i-1), l8%a2+141*(i-1), l8%a3+141*(i-1), l8%a4+141*(i-1), l8%a5+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i,'L9 ]'
     write(3,*) l9%a1+141*(i-1), l9%a2+141*(i-1), l9%a3+141*(i-1), l9%a4+141*(i-1), l9%a5+141*(i-1), l9%a6+141*(i-1)
     write(3,*)
     
     i = i + 1
     
  end do
  
  i = 1

  do while ( i <= 128 )  
     
     write(3,'(a2,i3,a4)') '[ ',i+128,'P1 ]'
     write(3,*) p1%a1+89578+141*(i-1), p1%a2+89578+141*(i-1), p1%a3+89578+141*(i-1), &
          p1%a4+89578+141*(i-1), p1%a5+89578+141*(i-1), p1%a6+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i+128,'P2 ]'
     write(3, *) p2%a1+89578+141*(i-1), p2%a2+89578+141*(i-1), p2%a3+89578+141*(i-1), &
          p2%a4+89578+141*(i-1), p2%a5+89578+141*(i-1), p2%a6+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'G1 ]'
     write(3,*) g1%a1+89578+141*(i-1), g1%a2+89578+141*(i-1), g1%a3+89578+141*(i-1), &
          g1%a4+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'G2 ]'
     write(3,*) g2%a1+89578+141*(i-1), g2%a2+89578+141*(i-1), g2%a3+89578+141*(i-1), &
          g2%a4+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'G3 ]'
     write(3,*) g3%a1+89578+141*(i-1), g3%a2+89578+141*(i-1), g3%a3+89578+141*(i-1), &
          g3%a4+89578+141*(i-1), g3%a5+89578+141*(i-1), g3%a6+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i+128,'L1 ]'
     write(3,*) l1%a1+89578+141*(i-1), l1%a2+89578+141*(i-1), l1%a3+89578+141*(i-1), &
          l1%a4+89578+141*(i-1), l1%a5+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i+128,'C1 ]'
     write(3,*) c1%a1+89578+141*(i-1), c1%a2+89578+141*(i-1), c1%a3+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'C2 ]'
     write(3,*) c2%a1+89578+141*(i-1), c2%a2+89578+141*(i-1), c2%a3+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'C3 ]'
     write(3,*) c3%a1+89578+141*(i-1), c3%a2+89578+141*(i-1), c3%a3+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'G4 ]'
     write(3,*) g4%a1+89578+141*(i-1), g4%a2+89578+141*(i-1), g4%a3+89578+141*(i-1), &
          g4%a4+89578+141*(i-1), g4%a5+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i+128,'C4 ]'
     write(3,*) c4%a1+89578+141*(i-1), c4%a2+89578+141*(i-1), c4%a3+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'C5 ]'
     write(3,*) c5%a1+89578+141*(i-1), c5%a2+89578+141*(i-1), c5%a3+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'C6 ]'
     write(3,*) c6%a1+89578+141*(i-1), c6%a2+89578+141*(i-1), c6%a3+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'C7 ]'
     write(3,*) c7%a1+89578+141*(i-1), c7%a2+89578+141*(i-1), c7%a3+89578+141*(i-1), c7%a4+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'C8 ]'
     write(3,*) c8%a1+89578+141*(i-1), c8%a2+89578+141*(i-1), c8%a3+89578+141*(i-1), c8%a4+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'L2 ]'
     write(3,*) l2%a1+89578+141*(i-1), l2%a2+89578+141*(i-1), l2%a3+89578+141*(i-1), &
          l2%a4+89578+141*(i-1), l2%a5+89578+141*(i-1), l2%a6+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'G5 ]'
     write(3,*) g5%a1+89578+141*(i-1), g5%a2+89578+141*(i-1), g5%a3+89578+141*(i-1), &
          g5%a4+89578+141*(i-1), g5%a5+89578+141*(i-1), g5%a6+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'L3 ]'
     write(3,*) l3%a1+89578+141*(i-1), l3%a2+89578+141*(i-1), l3%a3+89578+141*(i-1), &
          l3%a4+89578+141*(i-1)
     write(3,*)
           
     write(3,'(a2,i3,a4)') '[ ',i+128,'G6 ]'
     write(3,*) g6%a1+89578+141*(i-1), g6%a2+89578+141*(i-1), g6%a3+89578+141*(i-1), &
          g6%a4+89578+141*(i-1), g6%a5+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i+128,'C9 ]'
     write(3,*) c9%a1+89578+141*(i-1), c9%a2+89578+141*(i-1), c9%a3+89578+141*(i-1) 
     write(3,*)
     
     write(3,'(a2,i3,a5)') '[ ',i+128,'C10 ]'
     write(3,*) c10%a1+89578+141*(i-1), c10%a2+89578+141*(i-1), c10%a3+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a5)') '[ ',i+128,'C11 ]'
     write(3,*) c11%a1+89578+141*(i-1), c11%a2+89578+141*(i-1), c11%a3+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a5)') '[ ',i+128,'C12 ]'
     write(3,*) c12%a1+89578+141*(i-1), c12%a2+89578+141*(i-1), c12%a3+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a5)') '[ ',i+128,'C13 ]'
     write(3,*) c13%a1+89578+141*(i-1), c13%a2+89578+141*(i-1), c13%a3+89578+141*(i-1), c13%a4+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a5)') '[ ',i+128,'C14 ]'
     write(3,*) c14%a1+89578+141*(i-1), c14%a2+89578+141*(i-1), c14%a3+89578+141*(i-1), c14%a4+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'P3 ]'
     write(3, *) p3%a1+89578+141*(i-1), p3%a2+89578+141*(i-1), p3%a3+89578+141*(i-1), &
          p3%a4+89578+141*(i-1), p3%a5+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i+128,'L4 ]'
     write(3,*) l4%a1+89578+141*(i-1), l4%a2+89578+141*(i-1), l4%a3+89578+141*(i-1), &
          l4%a4+89578+141*(i-1), l4%a5+89578+141*(i-1), l4%a6+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'L5 ]'
     write(3,*) l5%a1+89578+141*(i-1), l5%a2+89578+141*(i-1), l5%a3+89578+141*(i-1), &
          l5%a4+89578+141*(i-1), l5%a5+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'L6 ]'
     write(3,*) l6%a1+89578+141*(i-1), l6%a2+89578+141*(i-1), l6%a3+89578+141*(i-1)
     write(3,*)
     
     write(3,'(a2,i3,a4)') '[ ',i+128,'P4 ]'
     write(3, *) p4%a1+89578+141*(i-1), p4%a2+89578+141*(i-1), p4%a3+89578+141*(i-1), &
          p4%a4+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'L7 ]'
     write(3,*) l7%a1+89578+141*(i-1), l7%a2+89578+141*(i-1), l7%a3+89578+141*(i-1), &
          l7%a4+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'L8 ]'
     write(3,*) l8%a1+89578+141*(i-1), l8%a2+89578+141*(i-1), l8%a3+89578+141*(i-1), &
          l8%a4+89578+141*(i-1), l8%a5+89578+141*(i-1)
     write(3,*)

     write(3,'(a2,i3,a4)') '[ ',i+128,'L9 ]'
     write(3,*) l9%a1+89578+141*(i-1), l9%a2+89578+141*(i-1), l9%a3+89578+141*(i-1), &
          l9%a4+89578+141*(i-1), l9%a5+89578+141*(i-1), l9%a6+89578+141*(i-1)
     write(3,*)
     
     i = i + 1
     
  end do

  close(3)
  
end program allmap
