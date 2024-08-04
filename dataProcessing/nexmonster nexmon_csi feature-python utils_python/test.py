from decoders import interleaved as decoder

samples = decoder.read_pcap('pcapfiles/long_run_0-7.pcap')

samples.csi # Access all CSI samples as a numpy matrix

print(samples.csi[0][0])