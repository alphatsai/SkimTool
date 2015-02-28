import FWCore.ParameterSet.Config as cms

ESTracksReducer = cms.EDProducer("ESTracksReducer",
                     generalTracksLabel      = cms.InputTag("generalTracks"),
                     generalTracksExtraLabel = cms.InputTag("generalTracks"),
		     trackingRecHitLabel     = cms.InputTag("generalTracks"),
                     newGeneralTracksCollection      = cms.string(''), 	# be endcap GeneralTracks 
                     newGeneralTracksExtraCollection = cms.string(''), 	# be endcap GeneralTrackExtras
                     newTrackingRecHitCollection     = cms.string(''), 	# be endcap TrackingRecHit
                   )
