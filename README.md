# RNW411 - ESPHome Replacement Board

Clone della scheda di controllo **RDZ RNW411** realizzata con ESP32 + ESPHome.

## Struttura repo

```
RNW411/
├── esphome/
│   └── rnw411.yaml          # Configurazione ESPHome completa
├── hardware/
│   ├── rnw411_skidl.py      # Schema KiCad via skidl
│   └── BOM.csv              # Bill of Materials
└── README.md
```

## Caratteristiche hardware

- **MCU**: ESP32-WROOM-32 (modulo)
- **ADC sonde**: ADS1115 (I2C, 16bit, 4 canali)
- **Alimentazione**: HLK-PM01 (230VAC→5V) + LDO AMS1117-3.3
- **Uscite**: Relè meccanici Omron G5LE-1-DC5 (5V bobina)
- **Protezioni**: Snubber RC lato AC, TVS + flyback su bobina, MOV su 230V ingresso
- **Connettori**: Phoenix 5.08mm su tutti i segnali
- **Ingressi digitali**: RC debounce 100Ω + 100nF + TVS SMAJ3V3A unidirezionale

## Ingressi

| Ingresso | Funzione | Note |
|----------|----------|------|
| S1 | Sonda NTC evaporatore (verde) | 10kΩ B=3435 |
| S2 | Sonda NTC acqua (giallo) | 10kΩ B=3435 |
| ID1 | Pressostato alta pressione (blu) | N.C., apre su allarme |
| ID2 | Consenso integrazione | Contatto pulito |
| ID3 | Consenso deumidificazione | Contatto pulito |
| ID4 | Consenso ventilazione | Contatto pulito |

## Uscite

| Uscita | Funzione | Protezioni |
|--------|----------|------------|
| OUT1 | Compressore | MOV + TVS + flyback + snubber RC |
| OUT2 | Valvola acqua | Snubber RC + flyback |
| OUT3 | Ventilatore vel. 1 | Snubber RC |
| OUT4 | Ventilatore vel. 2 | Snubber RC |
| OUT5 | Ventilatore vel. 3 | Snubber RC |

## Sicurezza

- Pressostato HP **in serie sulla bobina** del relè compressore (interlock hardware)
- Anti-corto-ciclo compressore: min 3 min OFF, 2 min ON
- Protezione antigelo: stop compressore se T_evap < -1°C
- Protezione alta T evaporatore: stop compressore se T_evap > 45°C per 30s con compressore ON
- Blocco permanente dopo 3 allarmi in 60 min → reset via Home Assistant
- Check sonda in errore (open/short): stop compressore su lettura fuori range

## Note di sicurezza PCB

- Clearance minima 230V: **8mm**
- Slot di isolamento sotto relè
- Connettori 230V marcati F/N/PE
- Fusibile 500mA su ingresso 230V
