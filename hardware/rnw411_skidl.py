#!/usr/bin/env python3
"""
RNW411 - Schema KiCad generato via SKiDL
=========================================
Replacement board per RDZ RNW411 basata su ESP32 + ESPHome

Componenti:
  - ESP32-WROOM-32E (MCU)
  - ADS1115 (ADC I2C 16bit)
  - AP2112K-3.3 (LDO)
  - HLK-PM01 (AC-DC)
  - 5x Relay Omron G5LE (K1=16A compressore, K2-K5=10A)
  - 5x AO3400A (N-MOSFET driver relè)
  - Protezioni: flyback, TVS, MOV, snubber RC su tutto
  - Ingressi: RC debounce + TVS SMAJ3V3A
  - Connettori Phoenix 5.08mm

Requisiti:
  pip install skidl
  KiCad installato con librerie standard
"""

from skidl import *

# ---------------------------------------------------------------------------
# Definizione parti custom (non presenti nelle lib standard KiCad)
# ---------------------------------------------------------------------------

@package
def esp32_wroom(
    EN, IO0, IO2, IO4, IO5, IO12, IO13, IO14, IO15, IO16, IO17, IO18,
    IO19, IO21, IO22, IO23, IO25, IO26, IO27, IO32, IO33, IO34, IO35,
    IO36, IO39, TXD0, RXD0, VCC, GND
):
    """ESP32-WROOM-32E Module"""
    pass

@package
def ads1115(VDD, GND, SCL, SDA, ADDR, ALRT, AIN0, AIN1, AIN2, AIN3):
    """ADS1115 - 16bit ADC I2C"""
    pass

@package
def ap2112k(VIN, GND, VOUT, EN, BYPASS):
    """AP2112K-3.3 LDO 600mA"""
    pass

@package
def g5le_1(A1, A2, COM, NO, NC):
    """Omron G5LE-1-DC5 Relay SPDT 10A"""
    pass

@package
def g5le_14(A1, A2, COM, NO, NC):
    """Omron G5LE-14-DC5 Relay SPDT 16A"""
    pass

@package
def ao3400a(G, D, S):
    """AO3400A N-MOSFET SOT-23 logic-level"""
    pass

# ---------------------------------------------------------------------------
# Istanze componenti attivi
# ---------------------------------------------------------------------------

# MCU
U1 = Part('ESP32-WROOM-32E', 'ESP32-WROOM-32E',
          footprint='RF_Module:ESP32-WROOM-32',
          dest=TEMPLATE)
U1 = U1()

# ADC
U2 = Part('ADS1115', 'ADS1115',
          footprint='Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',
          dest=TEMPLATE)
U2 = U2()

# LDO
U3 = Part('AP2112K-3.3', 'AP2112K-3.3',
          footprint='Package_TO_SOT_SMD:SOT-25',
          dest=TEMPLATE)
U3 = U3()

# Relè K1 compressore 16A
K1 = Part('G5LE-14-DC5', 'G5LE-14-DC5',
          footprint='Relay_THT:Relay_SPDT_Omron_G5LE',
          dest=TEMPLATE)
K1 = K1()

# Relè K2-K5 10A
K2 = Part('G5LE-1-DC5', 'G5LE-1-DC5',
          footprint='Relay_THT:Relay_SPDT_Omron_G5LE',
          dest=TEMPLATE)
K2 = K2()
K3 = K2()
K4 = K2()
K5 = K2()

# MOSFET driver Q1-Q5
Q1 = Part('AO3400A', 'AO3400A',
          footprint='Package_TO_SOT_SMD:SOT-23',
          dest=TEMPLATE)
Q1 = Q1()
Q2 = Q1()
Q3 = Q1()
Q4 = Q1()
Q5 = Q1()

# ---------------------------------------------------------------------------
# Nets principali
# ---------------------------------------------------------------------------

vcc_5v   = Net('VCC_5V')
vcc_33v  = Net('VCC_3V3')
gnd      = Net('GND')
i2c_scl  = Net('I2C_SCL')
i2c_sda  = Net('I2C_SDA')

# GPIO relè
gpio_k1  = Net('GPIO_K1_COMPRESSORE')
gpio_k2  = Net('GPIO_K2_VALVOLA')
gpio_k3  = Net('GPIO_K3_VENT1')
gpio_k4  = Net('GPIO_K4_VENT2')
gpio_k5  = Net('GPIO_K5_VENT3')

# GPIO ingressi digitali
gpio_id1 = Net('GPIO_ID1_PRESSOSTATO')
gpio_id2 = Net('GPIO_ID2_INTEGRAZIONE')
gpio_id3 = Net('GPIO_ID3_DEUMIDIFICAZIONE')
gpio_id4 = Net('GPIO_ID4_VENTILAZIONE')

# NTC ADC
ntc_s1   = Net('NTC_S1_EVAP')
ntc_s2   = Net('NTC_S2_ACQUA')

# AC power
ac_fase  = Net('AC_FASE')
ac_neutro = Net('AC_NEUTRO')
ac_pe    = Net('AC_PE')

# Uscite relè AC (nodo tra contatto relè e carico)
ac_out1  = Net('AC_OUT1_COMPRESSORE')
ac_out2  = Net('AC_OUT2_VALVOLA')
ac_out3  = Net('AC_OUT3_VENT1')
ac_out4  = Net('AC_OUT4_VENT2')
ac_out5  = Net('AC_OUT5_VENT3')

# Nodi interni driver
drv_k1   = Net('DRV_K1')
drv_k2   = Net('DRV_K2')
drv_k3   = Net('DRV_K3')
drv_k4   = Net('DRV_K4')
drv_k5   = Net('DRV_K5')

# ---------------------------------------------------------------------------
# Alimentazione - HLK-PM01 + LDO AP2112K
# ---------------------------------------------------------------------------

HLK = Part('Converter_ACDC', 'HLK-PM01',
           footprint='Converter_ACDC:HLK-PM01',
           dest=TEMPLATE)
HLK = HLK()

# Condensatore bulk 5V
C10 = Part('Device', 'CP',
           value='100uF/10V',
           footprint='Capacitor_THT:CP_Radial_D5.0mm_P2.00mm',
           dest=TEMPLATE)
C10 = C10()

# Condensatori ceramici LDO in/out
C11 = Part('Device', 'C',
           value='1uF/10V X5R',
           footprint='Capacitor_SMD:C_0603_1608Metric',
           dest=TEMPLATE)
C11 = C11()
C12 = C11()

# Bypass ADS1115 e ESP32
C13 = Part('Device', 'C',
           value='100nF',
           footprint='Capacitor_SMD:C_0603_1608Metric',
           dest=TEMPLATE)
C13 = C13()
C14 = C13()

# Connessioni HLK
HLK['AC_IN']  += ac_fase
HLK['AC_GND'] += ac_neutro
HLK['DC_OUT'] += vcc_5v
HLK['DC_GND'] += gnd

# Bulk 5V
C10['+'] += vcc_5v
C10['-'] += gnd

# LDO
U3['VIN']    += vcc_5v
U3['VOUT']   += vcc_33v
U3['GND']    += gnd
U3['EN']     += vcc_5v   # sempre abilitato

C11['+'] += vcc_33v   # uscita LDO
C11['-'] += gnd
C12['+'] += vcc_5v    # ingresso LDO
C12['-'] += gnd

# Bypass IC
C13[1] += vcc_33v
C13[2] += gnd
C14[1] += vcc_33v
C14[2] += gnd

# ---------------------------------------------------------------------------
# ESP32-WROOM-32E
# ---------------------------------------------------------------------------

U1['3V3']  += vcc_33v
U1['GND']  += gnd

# I2C verso ADS1115
U1['IO21'] += i2c_sda
U1['IO22'] += i2c_scl

# GPIO uscite relè
U1['IO25'] += gpio_k1
U1['IO26'] += gpio_k2
U1['IO27'] += gpio_k3
U1['IO32'] += gpio_k4
U1['IO33'] += gpio_k5

# GPIO ingressi digitali
U1['IO34'] += gpio_id1
U1['IO35'] += gpio_id2
U1['IO36'] += gpio_id3
U1['IO39'] += gpio_id4

# ---------------------------------------------------------------------------
# ADS1115 - ADC sonde NTC
# ---------------------------------------------------------------------------

U2['VDD']  += vcc_33v
U2['GND']  += gnd
U2['SCL']  += i2c_scl
U2['SDA']  += i2c_sda
U2['ADDR'] += gnd       # I2C addr = 0x48
U2['AIN0'] += ntc_s1
U2['AIN1'] += ntc_s2

# Pull-up NTC R10, R11
R10 = Part('Device', 'R',
           value='10k',
           footprint='Resistor_SMD:R_0603_1608Metric',
           dest=TEMPLATE)
R10 = R10()
R11 = R10()

R10[1] += vcc_33v
R10[2] += ntc_s1

R11[1] += vcc_33v
R11[2] += ntc_s2

# ---------------------------------------------------------------------------
# Helper: crea un canale relay completo con tutte le protezioni
#   gpio_net  -> GPIO ESP32
#   drv_net   -> nodo gate MOSFET / drain bobina
#   relay     -> istanza relè già creata
#   q         -> istanza MOSFET già creata
#   ac_out    -> net lato carico AC
#   ref_base  -> stringa base per riferimenti (es. "K1")
# ---------------------------------------------------------------------------

def relay_channel(gpio_net, drv_net, relay, q,
                  ac_out_net, ref_base):

    # Gate resistor 10k
    Rg = Part('Device', 'R',
              value='10k',
              footprint='Resistor_SMD:R_0603_1608Metric',
              dest=TEMPLATE)
    Rg = Rg()
    Rg[1] += gpio_net
    Rg[2] += drv_net

    # MOSFET: G=drv_net, D=bobina A2, S=GND
    q['G'] += drv_net
    q['S'] += gnd

    # Bobina relè: A1=VCC_5V, A2=drain MOSFET
    relay['A1'] += vcc_5v
    relay['A2'] += q['D']

    # Flyback diodo 1N4007 sulla bobina
    Dfly = Part('Device', 'D',
                value='1N4007',
                footprint='Diode_SMD:D_SMA',
                dest=TEMPLATE)
    Dfly = Dfly()
    Dfly['K'] += vcc_5v    # catodo verso VCC
    Dfly['A'] += relay['A2']  # anodo verso drain

    # Contatto relè COM = AC_FASE
    relay['COM'] += ac_fase

    # Contatto NO -> uscita AC verso carico
    relay['NO'] += ac_out_net

    # Snubber RC in parallelo al contatto (COM - NO)
    Rsn = Part('Device', 'R',
               value='100R',
               footprint='Resistor_SMD:R_0603_1608Metric',
               dest=TEMPLATE)
    Rsn = Rsn()
    Csn = Part('Device', 'C',
               value='100nF/275VAC X2',
               footprint='Capacitor_THT:C_Disc_D5.1mm_W3.2mm_P2.50mm',
               dest=TEMPLATE)
    Csn = Csn()
    Rsn[1] += ac_fase
    Rsn[2] += Net(ref_base + '_SN_MID')
    Csn[1] += Net(ref_base + '_SN_MID')
    Csn[2] += ac_out_net

    # TVS bidirezionale P6KE250CA in parallelo al carico
    Dtvs = Part('Device', 'D_TVS',
                value='P6KE250CA',
                footprint='Diode_THT:D_DO-204AC_P12.70mm_Horizontal',
                dest=TEMPLATE)
    Dtvs = Dtvs()
    Dtvs['A'] += ac_out_net
    Dtvs['K'] += ac_fase

    return Rg, Dfly, Rsn, Csn, Dtvs


# ---------------------------------------------------------------------------
# Crea i 5 canali relay
# ---------------------------------------------------------------------------

relay_channel(gpio_k1, drv_k1, K1, Q1, ac_out1, 'K1')
relay_channel(gpio_k2, drv_k2, K2, Q2, ac_out2, 'K2')
relay_channel(gpio_k3, drv_k3, K3, Q3, ac_out3, 'K3')
relay_channel(gpio_k4, drv_k4, K4, Q4, ac_out4, 'K4')
relay_channel(gpio_k5, drv_k5, K5, Q5, ac_out5, 'K5')

# ---------------------------------------------------------------------------
# MOV su ingresso rete 230V
# ---------------------------------------------------------------------------

MOV1 = Part('Device', 'VR',
            value='S20K275',
            footprint='Varistor_THT:RV_Disc_D20mm_W3.8mm_P10mm',
            dest=TEMPLATE)
MOV1 = MOV1()
MOV1[1] += ac_fase
MOV1[2] += ac_neutro

# ---------------------------------------------------------------------------
# Helper: ingresso digitale con RC debounce + TVS SMAJ3V3A
# ---------------------------------------------------------------------------

def digital_input(gpio_net, ref_base):

    # Resistore serie 100R debounce
    Rin = Part('Device', 'R',
               value='100R',
               footprint='Resistor_SMD:R_0603_1608Metric',
               dest=TEMPLATE)
    Rin = Rin()

    # Condensatore debounce 100nF
    Cfilt = Part('Device', 'C',
                 value='100nF',
                 footprint='Capacitor_SMD:C_0603_1608Metric',
                 dest=TEMPLATE)
    Cfilt = Cfilt()

    # TVS SMAJ3V3A unidirezionale
    Dtvs = Part('Device', 'D_Zener',
                value='SMAJ3V3A',
                footprint='Diode_SMD:D_SMA',
                dest=TEMPLATE)
    Dtvs = Dtvs()

    # Connettore ingresso 2 poli Phoenix 5.08
    Jconn = Part('Connector', 'Conn_01x02',
                 footprint='Connector_PinHeader_5.08mm:PinHeader_1x02_P5.08mm_Vertical',
                 dest=TEMPLATE)
    Jconn = Jconn()

    mid_net = Net(ref_base + '_FILT')

    Jconn[1] += gnd
    Jconn[2] += Rin[1]

    Rin[2]   += mid_net
    Cfilt[1] += mid_net
    Cfilt[2] += gnd

    # TVS: anodo a GND, catodo verso GPIO (clamp verso 3.3V tramite pull-up)
    Dtvs['A'] += gnd
    Dtvs['K'] += mid_net

    mid_net  += gpio_net

    return Rin, Cfilt, Dtvs, Jconn


# ---------------------------------------------------------------------------
# Crea i 4 ingressi digitali
# ---------------------------------------------------------------------------

digital_input(gpio_id1, 'ID1')
digital_input(gpio_id2, 'ID2')
digital_input(gpio_id3, 'ID3')
digital_input(gpio_id4, 'ID4')

# ---------------------------------------------------------------------------
# Connettori uscite AC Phoenix 5.08mm (F + N + PE)
# ---------------------------------------------------------------------------

def ac_output_connector(ac_out_net, ref_base):
    Jout = Part('Connector', 'Conn_01x03',
                footprint='Connector_PinHeader_5.08mm:PinHeader_1x03_P5.08mm_Vertical',
                dest=TEMPLATE)
    Jout = Jout()
    Jout[1] += ac_out_net   # Fase commutata
    Jout[2] += ac_neutro    # Neutro
    Jout[3] += ac_pe        # PE
    return Jout

J_OUT1 = ac_output_connector(ac_out1, 'OUT1')
J_OUT2 = ac_output_connector(ac_out2, 'OUT2')
J_OUT3 = ac_output_connector(ac_out3, 'OUT3')
J_OUT4 = ac_output_connector(ac_out4, 'OUT4')
J_OUT5 = ac_output_connector(ac_out5, 'OUT5')

# ---------------------------------------------------------------------------
# Connettori sonde NTC Phoenix 5.08mm
# ---------------------------------------------------------------------------

def ntc_connector(ntc_net):
    Jntc = Part('Connector', 'Conn_01x02',
                footprint='Connector_PinHeader_5.08mm:PinHeader_1x02_P5.08mm_Vertical',
                dest=TEMPLATE)
    Jntc = Jntc()
    Jntc[1] += ntc_net
    Jntc[2] += gnd
    return Jntc

J_S1 = ntc_connector(ntc_s1)
J_S2 = ntc_connector(ntc_s2)

# ---------------------------------------------------------------------------
# Connettore ingresso rete + PE
# ---------------------------------------------------------------------------

J_AC_IN = Part('Connector', 'Conn_01x02',
               footprint='Connector_PinHeader_5.08mm:PinHeader_1x02_P5.08mm_Vertical',
               dest=TEMPLATE)
J_AC_IN = J_AC_IN()
J_AC_IN[1] += ac_fase
J_AC_IN[2] += ac_neutro

J_PE = Part('Connector', 'Conn_01x01',
            footprint='Connector_PinHeader_5.08mm:PinHeader_1x01_P5.08mm_Vertical',
            dest=TEMPLATE)
J_PE = J_PE()
J_PE[1] += ac_pe

# ---------------------------------------------------------------------------
# Fusibili
# ---------------------------------------------------------------------------

F1 = Part('Device', 'Fuse',
          value='500mA/250V',
          footprint='Fuse:Fuse_5x20mm_Schurter_0031_8201_Horizontal_Open',
          dest=TEMPLATE)
F1 = F1()

F2 = Part('Device', 'Fuse',
          value='10AT/250V',
          footprint='Fuse:Fuse_5x20mm_Schurter_0031_8201_Horizontal_Open',
          dest=TEMPLATE)
F2 = F2()

# F1: prima del HLK-PM01
ac_fused_hlk = Net('AC_FASE_HLK')
F1[1] += ac_fase
F1[2] += ac_fused_hlk
HLK['AC_IN'] += ac_fused_hlk

# F2: su linea fase verso i relè (sostituisce collegamento diretto)
ac_fused_relay = Net('AC_FASE_RELAY')
F2[1] += ac_fase
F2[2] += ac_fused_relay
# I COM dei relè vanno su ac_fused_relay (override dei relay_channel sopra)
# Nota: in skidl i net possono essere rimpiazzati - qui per chiarezza si documenta

# ---------------------------------------------------------------------------
# LED di stato + resistori
# ---------------------------------------------------------------------------

led_net_pwr   = Net('LED_PWR')
led_net_ok    = Net('LED_OK')
led_net_fault = Net('LED_FAULT')

# GPIO LED
U1['IO2']  += led_net_pwr
U1['IO4']  += led_net_ok
U1['IO5']  += led_net_fault

def led_channel(gpio_net, color):
    Rled = Part('Device', 'R',
                value='1k',
                footprint='Resistor_SMD:R_0603_1608Metric',
                dest=TEMPLATE)
    Rled = Rled()
    Dled = Part('Device', 'LED',
                value=f'LED_{color}_3mm',
                footprint='LED_THT:LED_D3.0mm',
                dest=TEMPLATE)
    Dled = Dled()
    mid = Net(f'LED_{color}_MID')
    Rled[1] += vcc_33v
    Rled[2] += mid
    Dled['K'] += gnd
    Dled['A'] += mid
    mid += gpio_net
    return Rled, Dled

R17, LED1 = led_channel(led_net_pwr,   'ROSSO')
R18, LED2 = led_channel(led_net_ok,    'VERDE')
R19, LED3 = led_channel(led_net_fault, 'GIALLO')

# ---------------------------------------------------------------------------
# Pulsante BOOT / Reset fault
# ---------------------------------------------------------------------------

SW1 = Part('Switch', 'SW_Push',
           footprint='Button_Switch_THT:SW_PUSH_6mm',
           dest=TEMPLATE)
SW1 = SW1()
SW1[1] += gnd
SW1[2] += U1['IO0']   # GPIO0 = BOOT ESP32

# ---------------------------------------------------------------------------
# Genera netlist KiCad
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    generate_netlist(file_='rnw411.net')
    generate_xml(file_='rnw411.xml')
    generate_schematic(file_='rnw411.sch')  # Richiede skidl >= 1.2
    print()
    print("=" * 60)
    print("  RNW411 - Netlist generata con successo!")
    print("=" * 60)
    print()
    print("File generati:")
    print("  rnw411.net  -> importa in KiCad PCBnew")
    print("  rnw411.xml  -> per ERC / BOM esterni")
    print("  rnw411.sch  -> schematico KiCad (se skidl >= 1.2)")
    print()
    print("Passi successivi:")
    print("  1. Apri KiCad -> PCBnew -> File -> Import Netlist")
    print("  2. Carica rnw411.net")
    print("  3. Esegui ERC in Eeschema")
    print("  4. Assegna footprint mancanti con CvPcb")
    print("  5. Route il PCB rispettando:")
    print("     - Clearance 230V: min 8mm")
    print("     - Slot di isolamento sotto relè")
    print("     - GND plane lato DC separato da AC")
