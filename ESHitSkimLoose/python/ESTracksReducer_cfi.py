import FWCore.ParameterSet.Config as cms

ESTracksReducer = cms.EDProducer("ESTracksReducer",
                     generalTracksLabel = cms.InputTag("generalTracks"),
                     redGeneralTrackCollection = cms.string('endcapGeneralTracks'),
                     generalTracksExtraLabel = cms.InputTag("generalTracksExtra"),
                     redGeneralTrackExtraCollection = cms.string('endcapGeneralTracksExtra'),
                  )
