import FWCore.ParameterSet.Config as cms

ESHitSkimLoose = cms.EDFilter("ESHitSkimLoose",
                     generalTracksLabel = cms.InputTag("generalTracks"),
                     esRecHitLabel     	= cms.InputTag("ecalPreshowerRecHit:EcalRecHitsES"),
                   )
