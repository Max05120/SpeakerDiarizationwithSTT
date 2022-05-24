import glob
import webrtcvad
import logging
import wavSplit
from deepspeech import Model
from timeit import default_timer as timer

'''
Load the pre-trained model into the memory
@param models: Output Grapgh Protocol Buffer file
@param alphabet: Alphabet.txt file
@param lm: Language model file
@param trie: Trie file

@Retval
Returns a list [DeepSpeech Object, Model Load Time, LM Load Time]
'''


def load_model(models, alphabet):
    N_FEATURES = 26
    N_CONTEXT = 9
    BEAM_WIDTH = 500
    LM_ALPHA = 0.85
    LM_BETA = 1.85

    model_load_start = timer()
    ds = Model("../speech-to-text/deepspeech-0.9.3-models.pbmm")
    lm_file_path = "../speech-to-text/deepspeech-0.9.3-models.scorer"
    ds.enableExternalScorer(lm_file_path)
    ds.setScorerAlphaBeta(LM_ALPHA,LM_BETA)
    ds.setBeamWidth(BEAM_WIDTH)
    # model_load_end = timer() - model_load_start
    # logging.debug("Loaded model in %0.3fs." % (model_load_end))

    # lm_load_start = timer()
    # ds.enableDecoderWithLM(alphabet, LM_ALPHA, LM_BETA)
    # lm_load_end = timer() - lm_load_start
    # logging.debug('Loaded language model in %0.3fs.' % (lm_load_end))

    return [ds , lm_file_path]


'''
Run Inference on input audio file
@param ds: Deepspeech object
@param audio: Input audio for running inference on
@param fs: Sample rate of the input audio file

@Retval:
Returns a list [Inference, Inference Time, Audio Length]

'''


def stt(ds, audio, fs):
    inference_time = 0.0
    audio_length = len(audio) * (1 / 16000)

    # Run Deepspeech
    logging.debug('Running inference...')
    inference_start = timer() 
    output = ds.stt(audio)
    inference_end = timer() - inference_start
    inference_time += inference_end
    logging.debug('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))

    return [output, inference_time]


'''
Resolve directory path for the models and fetch each of them.
@param dirName: Path to the directory containing pre-trained models

@Retval:
Retunns a tuple containing each of the model files (pb, alphabet, lm and trie)
'''


def resolve_models(dirName):
    pb = glob.glob(dirName + "/*.pb")
    logging.debug("Found Model: %s" % pb)

    alphabet = glob.glob(dirName + "/alphabet.txt")
    logging.debug("Found Alphabet: %s" % alphabet)

    lm = glob.glob(dirName + "/lm.binary")
    trie = glob.glob(dirName + "/trie")
    logging.debug("Found Language Model: %s" % lm)
    logging.debug("Found Trie: %s" % trie)

    return pb, alphabet, lm, trie


'''
Generate VAD segments. Filters out non-voiced audio frames.
@param waveFile: Input wav file to run VAD on.0

@Retval:
Returns tuple of
    segments: a bytearray of multiple smaller audio frames
              (The longer audio split into mutiple smaller one's)
    sample_rate: Sample rate of the input audio file
    audio_length: Duraton of the input audio file

'''


def vad_segment_generator(wavFile, aggressiveness, frame_duration_ms=30, padding_duration_ms=300):
    logging.debug("Caught the wav file @: %s" % (wavFile))
    audio, sample_rate, audio_length = wavSplit.read_wave(wavFile)
    assert sample_rate == 16000, "Only 16000Hz input WAV files are supported for now!"
    vad = webrtcvad.Vad(int(aggressiveness))
    frames = wavSplit.frame_generator(frame_duration_ms, audio, sample_rate)
    frames = list(frames)
    segments = wavSplit.vad_collector(sample_rate, frame_duration_ms, padding_duration_ms, vad, frames)

    return [segment for segment in segments], sample_rate, audio_length
