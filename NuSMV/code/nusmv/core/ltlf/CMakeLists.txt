set(SRCS
  ltlf.c
  ltlf2smv/ltlf2smv.c
  )

nusmv_add_pkg_lib(${SRCS})

nusmv_add_pkg_headers(ltlf.h ltlf2smv/ltlf2smv.h)
