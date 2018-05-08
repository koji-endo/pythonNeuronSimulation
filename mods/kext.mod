NEURON {
  SUFFIX kext
  USEION k READ ik WRITE ko
  GLOBAL kbath
  RANGE fhspace, txfer
}

UNITS {
  (mA) = (milliamp)
  (mV) = (millivolt)
  (molar) = (1/liter)
  (mM)	= (millimolar)
  (nM)        = (nanomolar)
  FARADAY = (faraday) (coulombs)  :units are really coulombs/mole
}

PARAMETER {
  kbath = 10 (mM)
  fhspace = 100 (angstrom)
  txfer = 50 (ms)
}

ASSIGNED { ik (mA/cm2) }
STATE { ko (mM) }
BREAKPOINT { SOLVE state METHOD cnexp }
DERIVATIVE state {
  ko' = (1e8)*ik/(fhspace*FARADAY) + (kbath - ko)/txfer
}
