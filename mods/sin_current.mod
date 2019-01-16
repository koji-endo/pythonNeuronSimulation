:Exponential rise current

NEURON {
  POINT_PROCESS SinCurrent
  RANGE st, en, amp, offset, delay, freqency, i, pi
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
    st (ms)
    en (ms)
    offset (nA)
    delay (ms)
    freqency (1/ms)
    amp (nA)
    pi = 3.1415926535
}

ASSIGNED {
  i (nA)
}

INITIAL {
  i = 0
}

BREAKPOINT {
  at_time(st)
  at_time(en)
  if(t >= st && t < en){
    i = offset + amp * cos(2*pi*freqency*(t - delay))
  }
  else{
    i = 0
  }
}
