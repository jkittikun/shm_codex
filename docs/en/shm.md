---
title: Structural Health Monitoring
description: Learning map for the Structural Health Monitoring module.
---

# Structural Health Monitoring

<p class="page-lead">
This module introduces the measurement and interpretation workflow used to infer structural condition from response data.
</p>

<div class="process-grid">
  <article class="process-card">
    <span>01</span>
    <h2>Measure response</h2>
    <p>Acceleration, displacement, strain, and environmental records are treated as engineering signals, not just plots.</p>
  </article>
  <article class="process-card">
    <span>02</span>
    <h2>Extract features</h2>
    <p>Frequency peaks, damping ratios, mode shapes, and time-domain indicators become compact structural descriptors.</p>
  </article>
  <article class="process-card">
    <span>03</span>
    <h2>Interpret change</h2>
    <p>Observed shifts are compared with expected behavior, uncertainty, loading conditions, and model predictions.</p>
  </article>
  <article class="process-card">
    <span>04</span>
    <h2>Decide next action</h2>
    <p>Monitoring results support inspection, modelling, maintenance, and research questions rather than replacing judgement.</p>
  </article>
</div>

## Learning map

| Unit | Topic | Interactive support |
| --- | --- | --- |
| 01 | Vibration signals and sampling | Signal synthesis lab |
| 02 | Frequency content and FFT resolution | FFT resolution lab |
| 03 | Damping and free decay | Damping lab |
| 04 | Mode shapes and sensor placement | Mode-shape lab |
| 05 | Sensor selection for building SHM | Sensor package guide |

## Sensor selection for building SHM

For building SHM, acceleration, velocity, and displacement response are all useful, but **accelerometers are usually the primary/default sensors** for dynamic monitoring under wind, earthquake, ambient vibration, and operational modal analysis. They are normally paired with environmental sensors and, when the monitoring goal requires local or static response, with displacement, strain, tilt, crack, or other local-damage sensors.

<div class="sensor-grid">
  <article class="sensor-card">
    <span class="tag">Acceleration</span>
    <h3>Primary dynamic response</h3>
    <p><strong>Instruments:</strong> force-balance, MEMS, piezoelectric, and triaxial accelerometers.</p>
    <p><strong>Building use:</strong> floor vibration, modal frequency, mode shape, damping, earthquake/wind response, and post-event assessment.</p>
    <p>Most common in building SHM. For high-rise buildings, low-noise sensors are important because tall buildings have long natural periods and small-amplitude vibration.</p>
  </article>
  <article class="sensor-card">
    <span class="tag tag--cyan">Velocity</span>
    <h3>Serviceability and vibration intensity</h3>
    <p><strong>Instruments:</strong> velocity transducer, geophone, velocimeter, and seismometer.</p>
    <p><strong>Building use:</strong> ambient vibration, vibration serviceability, seismic response, and machinery/traffic-induced vibration.</p>
    <p>Useful in building monitoring, but usually less central than accelerometers.</p>
  </article>
  <article class="sensor-card">
    <span class="tag tag--magenta">Displacement / drift</span>
    <h3>Global deformation</h3>
    <p><strong>Instruments:</strong> LVDT, draw-wire potentiometer, laser displacement sensor, optical drift meter, GNSS/GPS, camera tracking, and crack/joint gauges.</p>
    <p><strong>Building use:</strong> interstory drift, roof displacement, settlement, joint movement, and residual deformation.</p>
    <p>Important for seismic performance, but harder to measure directly in occupied buildings. Double integration of acceleration is sensitive to baseline offsets and drift.</p>
  </article>
  <article class="sensor-card">
    <span class="tag">Strain</span>
    <h3>Member-level behavior</h3>
    <p><strong>Instruments:</strong> electrical resistance strain gauge, vibrating-wire strain gauge, and fiber Bragg grating / fiber-optic strain sensor.</p>
    <p><strong>Building use:</strong> member stress/strain, column/core-wall response, beam-column joints, construction-stage monitoring, and long-term deformation.</p>
    <p>Often combined with accelerometers to detect local behavior that vibration data alone may miss.</p>
  </article>
  <article class="sensor-card">
    <span class="tag tag--cyan">Tilt / rotation</span>
    <h3>Residual rotation</h3>
    <p><strong>Instruments:</strong> tiltmeter, inclinometer, MEMS tilt sensor, and gyroscope.</p>
    <p><strong>Building use:</strong> foundation rotation, wall/core tilt, residual deformation, and settlement-related rotation.</p>
    <p>Useful in high-rise, heritage, and post-event monitoring where residual rotation matters.</p>
  </article>
  <article class="sensor-card">
    <span class="tag tag--magenta">Crack / joint opening</span>
    <h3>Local damage</h3>
    <p><strong>Instruments:</strong> crack meter, displacement gauge, vibrating-wire crack gauge, and optical crack monitoring.</p>
    <p><strong>Building use:</strong> masonry/concrete cracking, facade movement, expansion joints, and post-earthquake damage.</p>
    <p>Useful for local damage, especially in reinforced concrete, masonry, and heritage buildings.</p>
  </article>
  <article class="sensor-card">
    <span class="tag">Temperature / humidity</span>
    <h3>Environmental compensation</h3>
    <p><strong>Instruments:</strong> thermocouple, RTD, and temperature/humidity logger.</p>
    <p><strong>Building use:</strong> environmental compensation, thermal drift correction, and durability monitoring.</p>
    <p>Essential because temperature and humidity can change modal properties and strain readings.</p>
  </article>
  <article class="sensor-card">
    <span class="tag tag--cyan">Wind / environmental loading</span>
    <h3>Response correlation</h3>
    <p><strong>Instruments:</strong> anemometer, wind vane, and barometer.</p>
    <p><strong>Building use:</strong> correlating building response with wind excitation and comfort/serviceability studies.</p>
    <p>Common for tall buildings where wind governs serviceability response.</p>
  </article>
  <article class="sensor-card">
    <span class="tag tag--magenta">Piezoelectric / acoustic / ultrasonic</span>
    <h3>Specialized local detection</h3>
    <p><strong>Instruments:</strong> PZT patch, acoustic emission sensor, and ultrasonic transducer.</p>
    <p><strong>Building use:</strong> crack initiation, impact detection, local damage, and debonding.</p>
    <p>More specialized; useful for local damage detection rather than global building vibration monitoring.</p>
  </article>
</div>

### Typical building SHM package

For a normal multi-story or high-rise building, a practical starter package is usually **triaxial accelerometers at selected floors**, plus **temperature/humidity sensors** for compensation. For performance-based monitoring or post-earthquake assessment, add **direct displacement/interstory drift sensors**, **strain gauges or FBG sensors** at critical members, and **tiltmeters** at foundation, core, or roof locations.

### Sources

- [Practical Implementation of Structural Health Monitoring in Multi-Story Buildings](https://www.mdpi.com/2075-5309/11/6/263)
- [Sensing Solutions for Structural Health Monitoring](https://www.epsondevice.com/sensing/en/applications/shm/)
- [USGS structural instrumentation guidance](https://pubs.usgs.gov/of/2000/0157/pdf/of00-157.pdf)
- [IIT Kanpur paper on displacement from acceleration](https://www.iitk.ac.in/nicee/wcee/article/14_11-0089.PDF)
- [Campbell Scientific structural health monitoring](https://www.campbellsci.com/structural-health-monitoring)
- [Structural Health Monitoring overview](https://www.sciencedirect.com/topics/physics-and-astronomy/structural-health-monitoring)
- [GeoSIG high-rise building SHM solutions](https://www.geosig.com/High-Rise-Buildings)

## Notes for future expansion

- Add field measurement examples once public datasets are ready.
- Add assignments as Markdown pages with downloadable CSV files.
- Add Thai-language teaching notes when authored and checked for terminology.
