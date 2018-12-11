:ribbon synapse
:graded synaptic transmission based on presynaptic voltage
: with delay

DEFINE BUFFER_SIZE 2048

NEURON {
  POINT_PROCESS rtolsyn
  RANGE vpre
  RANGE vth, vre, k, gsat, n, g, numsyn
  RANGE delay,buf_idx,diffvolt,basevolt,tau
  NONSPECIFIC_CURRENT i
  THREADSAFE
  POINTER ptr
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
  vth = -80(mV)
  k = 20 (nS/mV)
  gsat = 800(nS)
  n = 1
  numsyn = 1
  diffvolt = 0(mV)
  basevolt = 50(mV)
  tau = 1.05
  vre = -80(mV)
}

STATE {
  gs[BUFFER_SIZE] (uS)
}

ASSIGNED {
  v (mV)
  g (uS)
  i (nA)
  vpre (mV)
  delay (ms)
  buf_idx
  ptr
}

VERBATIM
#define BUFFER_SIZE 2048

typedef struct {
  int delay_flame;
} Delay;
ENDVERBATIM

CONSTRUCTOR {
VERBATIM
  Delay** ip = (Delay**)(&_p_ptr);
  Delay* dflame = (Delay*)hoc_Emalloc(sizeof(dflame)); hoc_malchk();
  *ip = dflame;
  dflame->delay_flame = (int)(delay / 0.0125);
ENDVERBATIM
}
DESTRUCTOR {
VERBATIM
  Delay** ip = (Delay**)(&_p_ptr);
  Delay* dflame = *ip;
  free(dflame);
ENDVERBATIM
}

INITIAL {
  FROM idx = 0 TO BUFFER_SIZE-1{
    gs[idx] = 0
  }
  buf_idx = 0
}
BREAKPOINT {
  if (vpre >= vth){
    g = k * pow((vpre - vth), n)
    if (g > gsat){
      g = gsat
    }
  }
  else {
    g = 0
  }
  if (vpre -basevolt > 3 || vpre-basevolt < -3){
    diffvolt = vpre - basevolt + diffvolt
    basevolt = vpre
  }
  VERBATIM
  int idx = 0;
  int delayed_address = 0;
  Delay** ip = (Delay**)(&_p_ptr);
  Delay* dflame = *ip;
  dflame->delay_flame = (int)(delay / 0.0125);
  delayed_address = ((int)buf_idx + dflame->delay_flame) % BUFFER_SIZE;
  gs[delayed_address] = g;
  i = gs[(int)buf_idx] * ((v - vre) + diffvolt) * numsyn;
  diffvolt = diffvolt/tau;
  buf_idx  = (int)(buf_idx + 1) % BUFFER_SIZE;
  ENDVERBATIM
}
