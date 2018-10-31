:Exponential rise current

NEURON {
  POINT_PROCESS ExpCurrent
  RANGE offset, amp, dur, tau, del, i
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
    tau (1/ms)
    dur (ms)
    del (ms)
    amp (nA)
    offset = 0 (nA)
}

ASSIGNED {
  i (nA)
}

INITIAL {
  i = 0
}

BREAKPOINT {
  at_time(del)
  at_time(del+dur)
  if(t >= del && t < del+dur){
    i = offset + (amp-offset) * (1 - exp(-1*tau*t))
  }
  else{
    i = 0
  }

}
