cmake_minimum_required(VERSION 3.17)
project(qdp_examples)

find_package(QDPXX REQUIRED)
	
add_executable(simple simple.cc)
add_executable(cb2 cb2.cc)



target_link_libraries( simple QDPXX::qdp)
target_link_libraries( cb2 QDPXX::qdp)



if (QDP_IS_QDPJIT)
  target_link_libraries(simple QDPXX::jit)
  target_link_libraries(cb2 QDPXX::jit)
  
  set_target_properties( simple PROPERTIES CXX_STANDARD 20 )
  set_target_properties( cb2 PROPERTIES CXX_STANDARD 20 )

  if( QDP_BACKEND_L0 )
    find_package(PkgConfig REQUIRED)
    pkg_search_module(PKG_LLVMSPIRV REQUIRED LLVMSPIRVLib)

    target_link_libraries(simple ${PKG_LLVMSPIRV_LIBRARIES})
    target_link_libraries(cb2 ${PKG_LLVMSPIRV_LIBRARIES})

    target_link_options(simple PUBLIC ${PKG_LLVMSPIRV_LDFLAGS})
    target_link_options(cb2 PUBLIC ${PKG_LLVMSPIRV_LDFLAGS})
  endif()
  
endif()





