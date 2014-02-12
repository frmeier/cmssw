import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")
# -- Load default module/services configurations -- //
# Message logger service
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cout = cms.untracked.PSet(
    threshold = cms.untracked.string('INFO'),
    default = cms.untracked.PSet(
        limit = cms.untracked.int32(10000000)
    )
)
#replace MessageLogger.debugModules = { "*" }

# Global Tag
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'START53_V27::All' # take your favourite

# This uses the object from the tag and applies the misalignment scenario on top of that object
process.load("Alignment.CommonAlignmentProducer.AlignmentProducer_cff")
process.AlignmentProducer.doMisalignmentScenario=True
process.AlignmentProducer.applyDbAlignment=True
from Alignment.TrackerAlignment.Scenarios_cff import *
process.AlignmentProducer.MisalignmentScenario = TrackerCSA14Scenario
process.AlignmentProducer.saveToDB=True
process.AlignmentProducer.saveApeToDB=True

# service = Tracer {}
# Ideal geometry producer
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")

process.load("Geometry.TrackerNumberingBuilder.trackerNumberingGeometry_cfi")

# Misalignment example scenario producer
# This works only if you like to produce something w.r.t. ideal
#process.load("Alignment.TrackerAlignment.MisalignedTracker_cfi")
#process.MisalignedTracker.saveToDbase = True # to store to DB
#import Alignment.TrackerAlignment.Scenarios_cff as _Scenarios
#process.MisalignedTracker.scenario = _Scenarios.TrackerCSA14Scenario
#process.MisalignedTracker.scenario = _Scenarios.Tracker10pbScenario
#process.MisalignedTracker.scenario = _Scenarios.SurveyLASOnlyScenario
#process.MisalignedTracker.scenario = _Scenarios.SurveyLASCosmicsScenario
#process.MisalignedTracker.scenario = _Scenarios.TrackerCRAFTScenario

# the module
process.prod = cms.EDAnalyzer("TestAnalyzer",
    fileName = cms.untracked.string('misaligned.root')
)

# data loop
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

# Database output service
import CondCore.DBCommon.CondDBSetup_cfi
process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    CondCore.DBCommon.CondDBSetup_cfi.CondDBSetup,
    # Writing to oracle needs the following shell variable setting (in zsh):
    # export CORAL_AUTH_PATH=/afs/cern.ch/cms/DB/conddb
    # connect = cms.string('oracle://cms_orcoff_prep/CMS_COND_ALIGNMENT'),  # preparation/develop. DB
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:Alignments.db'),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerCSA14Scenario')
    ), 
        cms.PSet(
            record = cms.string('TrackerAlignmentErrorRcd'),
            tag = cms.string('TrackerCSA14ScenarioErrors')
        ))
)
process.PoolDBOutputService.DBParameters.messageLevel = 2

process.p1 = cms.Path(process.prod)



