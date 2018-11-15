:Exponential rise current

NEURON {
  POINT_PROCESS BellCurrent
  RANGE st, en, amp, slope, i
  ELECTRODE_CURRENT i
}

UNITS {
    (mA) = (milliamp)
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (S)  = (siemens)
    (uS) = (microsiemens)
    (nS) = (nanosiemens)
    (molar) = (1/liter)
    (mM)	= (millimolar)
    (nM)        = (nanomolar)
    FARADAY = (faraday) (coulomb)  :units are really coulombs/mole
    PI	= (pi) (1)
}

PARAMETER {
    slope (1/ms)
    st (ms)
    en (ms)
    amp (nA)
}

ASSIGNED {
  i (nA)
  a
  b
  c
}

INITIAL {
  i = 0
}

BREAKPOINT {
    c = (st+en)/2
    a = (en-st)/2
    b = 2 * a * slope
    i = amp/(1 + pow(abso((t-c)/a),2*b))
}

FUNCTION abso(x){
  if(x>=0){
    abso = x
  }
  else{
    abso = -x
  }
}
