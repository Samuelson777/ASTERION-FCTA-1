export const versions = [
  {
    id: 'v0.1', label: '0.1', title: 'Project Definition', phase: 'Foundation',
    status: 'Baseline established', modelMode: 'procedural', model: null,
    summary: 'Mission definition, design boundaries, requirements, risk register and the first parametric sizing logic.',
    skills: ['Systems engineering','Requirements','Risk management','Python sizing'],
    metrics: [
      ['Requirements','34','traceable'], ['Ring radius','12 m','reference'], ['Artificial gravity','0.248 g','at 4.3 rpm'], ['Power target','200–300 kW','at 1 AU']
    ],
    progress: {cad:10, cae:5, cam:0, docs:35},
    results: [
      {label:'Architecture definition', value:100, suffix:'%'},
      {label:'Native CAD maturity', value:5, suffix:'%'},
      {label:'Verification coverage', value:8, suffix:'%'}
    ],
    notes: ['Orbit-assembled architecture selected.','Unrestricted-travel claims explicitly rejected.','Electric propulsion and visible thermal control adopted.'],
    gallery: [], deliverables: [
      ['Project charter','assets/docs/ASTERION_FCTA_1_Final_Engineering_Report_v1_0.md'],
      ['Complete v1.0 release','downloads/asterion-fcta-v1.0-public-release.zip']
    ]
  },
  {
    id:'v0.2', label:'0.2', title:'NX Master Skeleton', phase:'Parametric CAD', status:'Neutral geometry generated',
    modelMode:'single', model:'assets/models/asterion-v0.2-master-envelope.glb',
    summary:'Top-down vehicle coordinate system, station planes, subsystem envelopes, interface points, WAVE publication map and NXOpen starter workflow.',
    skills:['NX expressions','Master model','WAVE linking','Interfaces','NXOpen'],
    metrics:[['Vehicle length','≈50 m','with Skimmer'],['Ring diameter','26 m','two rings'],['Solar span','58 m','reference'],['Mesh faces','15,766','neutral model']],
    progress:{cad:32,cae:8,cam:0,docs:48},
    results:[{label:'CAD envelope complete',value:82,suffix:'%'},{label:'Interface definition',value:75,suffix:'%'},{label:'Native feature history',value:15,suffix:'%'}],
    notes:['Stable station identifiers introduced.','Six propulsion and six radiator interfaces defined.','Neutral GLB/STL/OBJ exports created.'],
    gallery:['assets/images/v02-plan.png'],
    deliverables:[['Tutorial drawings','assets/docs/ASTERION_FCTA_1_Full_Tutorial_Drawings.pdf'],['Native CAD builder','downloads/asterion-native-cad-builder-v1.1-fixed.zip']]
  },
  {
    id:'v0.3', label:'0.3', title:'Primary Structure', phase:'Structural CAD', status:'Beam model validated',
    modelMode:'single', model:'assets/models/asterion-v0.3-primary-structure.glb',
    summary:'Eight-longeron central truss, ring supports, docking load frame, propulsion frame and ANSYS-ready beam idealisation.',
    skills:['NX structure design','Beam idealisation','Material sizing','APDL preparation'],
    metrics:[['Nodes','222','structural'],['Beam elements','580','baseline'],['Tube families','7','sections'],['Idealised mass','7.74 t','tubes only']],
    progress:{cad:50,cae:28,cam:0,docs:58},
    results:[{label:'Topology validation',value:100,suffix:'%'},{label:'Load path definition',value:80,suffix:'%'},{label:'Detailed joint modelling',value:20,suffix:'%'}],
    notes:['Zero-length beam issue detected and corrected.','Twin 12-spoke ring supports included.','Separate docking and propulsion load frames created.'],
    gallery:['assets/images/v03-structure-plan.png'],
    deliverables:[['Engineering report','assets/docs/ASTERION_FCTA_1_Final_Engineering_Report_v1_0.md']]
  },
  {
    id:'v0.4', label:'0.4', title:'Integrated Spacecraft Assembly', phase:'Digital Mock-up', status:'Full neutral assembly complete',
    modelMode:'single', model:'assets/models/asterion-v0.4-full-assembly.glb',
    summary:'Integrated spacecraft with habitats, solar arrays, radiators, propulsion, tanks, docking, robotic servicing and the Skimmer aeroshuttle.',
    skills:['NX assemblies','Arrangements','Mass properties','Clearance','BOM'],
    metrics:[['Dry mass','50.54 t','screening'],['Full mass','62.54 t','with propellant'],['GLB objects','147','named'],['Solar span','57.8 m','validated']],
    progress:{cad:72,cae:38,cam:5,docs:66},
    results:[{label:'Assembly integration',value:92,suffix:'%'},{label:'Mass model',value:86,suffix:'%'},{label:'Interface reconciliation',value:82,suffix:'%'}],
    notes:['59 mass-model components integrated.','Dry and loaded CG cases computed.','Remote-mass definitions prepared for ANSYS.'],
    gallery:['assets/images/v04-full-isometric.png'],
    deliverables:[['Design review deck','assets/docs/ASTERION_FCTA_1_v0_9_Design_Review.pptx'],['Full tutorial drawings','assets/docs/ASTERION_FCTA_1_Full_Tutorial_Drawings.pdf']]
  },
  {
    id:'v0.5', label:'0.5', title:'Structural Analysis', phase:'ANSYS / Correlation', status:'Screening exposed redesign needs',
    modelMode:'single', model:'assets/models/asterion-v0.3-primary-structure.glb', overlay:'loads',
    summary:'Static, modal and buckling workflow with an independent Python frame solver for correlation and design screening.',
    skills:['ANSYS Mechanical','Modal analysis','Buckling','Python FEA','Correlation'],
    metrics:[['Load cases','7','static'],['First mode','0.1308 Hz','supported'],['Propulsion deflection','13.79 mm','near limit'],['Docking deflection','52.82 mm','redesign']],
    progress:{cad:72,cae:62,cam:5,docs:73},
    results:[
      {label:'Docking compression',value:95,suffix:'%'},
      {label:'Propulsion stiffness',value:62,suffix:'%'},
      {label:'Misaligned docking',value:28,suffix:'%'},
      {label:'Ring emergency braking',value:18,suffix:'%'}
    ],
    notes:['Emergency braking and lateral docking were not hidden as failures.','First supported flexible mode was above the provisional minimum.','Joint and shell effects remained outside the beam model.'],
    gallery:['assets/images/v05-displacement.png','assets/images/v05-modal.png'],
    deliverables:[['Final report','assets/docs/ASTERION_FCTA_1_Final_Engineering_Report_v1_0.md']]
  },
  {
    id:'v0.6', label:'0.6', title:'Thermal and CFD Studies', phase:'Multiphysics', status:'Reduced-order workflows complete',
    modelMode:'single', model:'assets/models/asterion-v0.6-analysis-models.glb',
    summary:'Radiator equilibrium, cold-plate and habitat-wall thermal studies, cabin ventilation and Skimmer external aerodynamics.',
    skills:['ANSYS Thermal','Fluent','Species transport','External aerodynamics','Mesh planning'],
    metrics:[['Radiator area','144 m²','effective'],['Nominal temperature','361.4 K','120 kW'],['Cabin CO₂','587 ppm','nominal'],['Skimmer studies','Mach 0.3–2','screening']],
    progress:{cad:75,cae:78,cam:5,docs:80},
    results:[{label:'Radiator nominal margin',value:82,suffix:'%'},{label:'Ventilation normal mode',value:90,suffix:'%'},{label:'Transonic confidence',value:42,suffix:'%'},{label:'Thermal-stress preparation',value:68,suffix:'%'}],
    notes:['Five-panel degraded radiator case reached about 378 K.','Fan-loss CO₂ reached 1000 ppm after about 27.9 minutes.','Mach 2 result is not re-entry aerothermodynamics.'],
    gallery:['assets/images/v06-radiator.png','assets/images/v06-co2.png','assets/images/v06-aero.png'],
    deliverables:[['Engineering report','assets/docs/ASTERION_FCTA_1_Final_Engineering_Report_v1_0.md']]
  },
  {
    id:'v0.7', label:'0.7', title:'NX CAM and Manufacturing', phase:'Manufacturing', status:'Four demonstrators prepared',
    modelMode:'manufacturing', models:[
      'assets/models/thruster-gimbal-bracket.glb','assets/models/ring-bearing-housing.glb','assets/models/skimmer-wing-rib.glb','assets/models/lightweight-bulkhead.glb'
    ],
    summary:'Representative milling, turning, thin-wall machining, fixtures, inspection plans, safe educational G-code and printable prototypes.',
    skills:['NX CAM','Milling','Turning','Fixtures','Inspection','Additive manufacturing'],
    metrics:[['CAM parts','4','demonstrators'],['Operations','12','planned'],['Tools','10','controlled'],['Cost estimate','£419.68','screening']],
    progress:{cad:80,cae:80,cam:78,docs:86},
    results:[{label:'CAM operation planning',value:92,suffix:'%'},{label:'Inspection planning',value:88,suffix:'%'},{label:'Machine-ready code',value:20,suffix:'%'},{label:'Prototype readiness',value:74,suffix:'%'}],
    notes:['G-code is simulation-only.','Exact machine, postprocessor, holders and fixtures remain mandatory.','STL prototypes include spacecraft, ring drive and docking latch.'],
    gallery:['assets/images/v07-gimbal-toolpath.png','assets/images/v07-bearing-toolpath.png'],
    deliverables:[['Tutorial drawing package','downloads/ASTERION_FCTA_1_Full_Tutorial_Drawings_Package.zip']]
  },
  {
    id:'v0.8', label:'0.8', title:'Optimisation and Redesign', phase:'Engineering Iteration', status:'H3 redesign selected',
    modelMode:'single', model:'assets/models/asterion-v0.8-optimised-structure.glb', overlay:'optimised',
    summary:'Design-of-experiments trade study added credible torque, docking and propulsion load paths while balancing structural mass.',
    skills:['Design optimisation','DOE','Structural redesign','Mass/CG update','Verification closure'],
    metrics:[['Beam elements','648','optimised'],['Structure mass','10.42 t','idealised'],['First mode','0.1964 Hz','+50.2%'],['Docking deflection','22.87 mm','−56.7%']],
    progress:{cad:90,cae:92,cam:80,docs:92},
    results:[{label:'Propulsion deflection reduction',value:98.4,suffix:'%'},{label:'Docking deflection reduction',value:56.7,suffix:'%'},{label:'Modal improvement',value:50.2,suffix:'%'},{label:'Mass efficiency',value:72,suffix:'%'}],
    notes:['48 ring torque braces added.','Eight docking spreaders and 12 propulsion struts added.','Counter-rotating braking torque direction corrected.'],
    gallery:['assets/images/v08-optimised-plan.png','assets/images/v08-comparison.png','assets/images/v08-modal.png'],
    deliverables:[['Final engineering report','assets/docs/ASTERION_FCTA_1_Final_Engineering_Report_v1_0.md']]
  },
  {
    id:'v0.9', label:'0.9', title:'Validation and Presentation', phase:'Design Review', status:'Portfolio evidence assembled',
    modelMode:'single', model:'assets/models/asterion-v0.4-full-assembly.glb',
    summary:'Requirements verification, final report, prototype test planning, design-review presentation and the first integrated browser viewer.',
    skills:['Verification','Design review','Technical report','Presentation','Web visualisation'],
    metrics:[['Review deck','1','complete'],['Report','1','engineering'],['Viewer models','7','interactive'],['Validation records','controlled','CSV/JSON']],
    progress:{cad:92,cae:94,cam:84,docs:98},
    results:[{label:'Portfolio evidence',value:96,suffix:'%'},{label:'Requirements traceability',value:88,suffix:'%'},{label:'Native solver evidence',value:35,suffix:'%'},{label:'Presentation readiness',value:100,suffix:'%'}],
    notes:['Evidence and claims separated.','Prototype test plan established.','Interactive browser models included.'],
    gallery:['assets/images/v04-full-isometric.png','assets/images/v08-comparison.png','assets/images/v06-aero.png'],
    deliverables:[['Design review presentation','assets/docs/ASTERION_FCTA_1_v0_9_Design_Review.pptx'],['Tutorial drawings','assets/docs/ASTERION_FCTA_1_Full_Tutorial_Drawings.pdf']]
  },
  {
    id:'v1.0', label:'1.0', title:'Public Open-Source Release', phase:'Publication', status:'GitHub-ready baseline',
    modelMode:'single', model:'assets/models/asterion-v0.4-full-assembly.glb',
    summary:'Clean public repository with release notes, licensing, citation metadata, reproducibility instructions, GitHub Pages and an artefact-status ledger.',
    skills:['Open-source release','GitHub Pages','Documentation','Reproducibility','Engineering ethics'],
    metrics:[['Repository files','449','baseline'],['GLB models','7','viewer'],['Release version','1.0.0','public'],['Native evidence','pending','owner execution']],
    progress:{cad:94,cae:94,cam:86,docs:100},
    results:[{label:'Public release readiness',value:100,suffix:'%'},{label:'Documentation coverage',value:100,suffix:'%'},{label:'Neutral artefact coverage',value:96,suffix:'%'},{label:'Native NX/ANSYS evidence',value:35,suffix:'%'}],
    notes:['MIT-licensed portfolio baseline.','Neutral geometry and screening results are clearly labelled.','Native NX and solved ANSYS evidence must be added from the owner’s workstation.'],
    gallery:['assets/images/v04-full-isometric.png','assets/images/v08-optimised-plan.png','assets/images/v06-radiator.png'],
    deliverables:[['Download public release','downloads/asterion-fcta-v1.0-public-release.zip'],['Native CAD builder','downloads/asterion-native-cad-builder-v1.1-fixed.zip'],['Full drawing package','downloads/ASTERION_FCTA_1_Full_Tutorial_Drawings_Package.zip']]
  }
];

export const subsystemPatterns = {
  all: [],
  structure: ['STRUCTURE','PRIMARY','SPINE','TRUSS','BRACE','LONGERON','FRAME','SPOKE','SUPPORT','E6'],
  habitat: ['HAB','RING','WHIPPLE','REFUGE'],
  propulsion: ['PROP','THRUST','RCS','POD','GIMBAL','TANK'],
  power: ['SOLAR','ARRAY','POWER'],
  thermal: ['RADIATOR','COLD_PLATE','THERMAL'],
  skimmer: ['SKIMMER','WING','ELEVON','FIN'],
  docking: ['DOCK','CAPTURE','LATCH'],
  robotics: ['ROBOT','ARM','JOINT'],
  analysis: ['RADIATOR_PANEL','COLD_PLATE','CABIN_ENCLOSURE','SKIMMER_SURFACE']
};
