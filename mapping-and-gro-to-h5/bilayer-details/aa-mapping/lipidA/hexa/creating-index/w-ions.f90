program allmap
  
  character*6 :: aux
  
  integer :: i, ierr, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, j

  open(1, file='index.ndx', status='old')
  open(2, file='vai.ndx', status='new')
  
  read(1, *, IOSTAT=ierr) aux

  i = 1

  do while ( i<= 17)

     read(1, *, IOSTAT=ierr) a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15
          
     write(2,*) '[ CA ]'
     write(2,*) a1

     write(2,*) '[ CA ]'
     write(2,*) a2
     
     write(2,*) '[ CA ]'
     write(2,*) a3
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a4
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a5
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a6
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a7
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a8
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a9
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a10
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a11
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a12
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a13
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a14
     write(*,*)
     
     write(2,*) '[ CA ]'
     write(2,*) a15
     write(*,*)
     
     i = i + 1

  end do

  read(1,*) a1
  write(2,*) '[ CA ]'
  write(2,*) a1
  write(*,*)

  read(1, *, IOSTAT=ierr) aux

  i = 1
  j = 1

    do while ( i<=637 )

     read(1, *, IOSTAT=ierr) a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15
          
     write(2,*) '[ W ]'
     write(2,*) a1

     write(2,*) '[ W ]'
     write(2,*) a5
     
     write(2,*) '[ W ]'
     write(2,*) a9
     write(*,*)
     
     write(2,*) '[ W ]'
     write(2,*) a13
     write(*,*)

     read(1, *, IOSTAT=ierr) a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15
     
     write(2,*) '[ W ]'
     write(2,*) a2
     write(*,*)
     
     write(2,*) '[ W ]'
     write(2,*) a6
     write(*,*)
     
     write(2,*) '[ W ]'
     write(2,*) a10
     write(*,*)

     write(2,*) '[ W ]'
     write(2,*) a14
     write(*,*)
     
     read(1, *, IOSTAT=ierr) a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15
     
     write(2,*) '[ W ]'
     write(2,*) a3
     write(*,*)
     
     write(2,*) '[ W ]'
     write(2,*) a7
     write(*,*)
     
     write(2,*) '[ W ]'
     write(2,*) a11
     write(*,*)
     
     write(2,*) '[ W ]'
     write(2,*) a15
     write(*,*)

     read(1, *, IOSTAT=ierr) a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15
     
     write(2,*) '[ W ]'
     write(2,*) a4
     write(*,*)
     
     write(2,*) '[ W ]'
     write(2,*) a8
     write(*,*)
     
     write(2,*) '[ W ]'
     write(2,*) a12
     write(*,*)
     
     i = i + 1

  end do

  read(1, *, IOSTAT=ierr) a1
  write(2,*) '[ W ]'
  write(2,*) a1
  
  close(1)
  close(2)
  
end program allmap
