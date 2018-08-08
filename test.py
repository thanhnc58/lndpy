import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc
import shlex
import os
from enum import Enum
from subprocess import Popen, PIPE, STDOUT, call
import time

file = open('test.in', 'r')
data = file.readlines()
for line in data:
    words = line.split()
    print data[1].split()



directory = "/Users/thanh_nc/lnd/simnet/"
os.chdir(directory)
os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'
processes = []
timeout = 0.1

command_line = "/Users/thanh_nc/go/bin/btcd --txindex --simnet --rpcuser=kek --rpcpass=kek --maxpeers=100 --rpcmaxwebsockets=100"

args = shlex.split(command_line)
btcd = Popen(args)
time.sleep(10)
n = 5
address = []

for i in range(n):
    os.chdir("/Users/thanh_nc/lnd/simnet/")
    call(["mkdir",str(i)])
    os.chdir("/Users/thanh_nc/lnd/simnet/" + str(i))
    port = str(i) if i >= 10 else '0' + str(i)
    command_line = "/Users/thanh_nc/go/src/github.com/lightningnetwork/lnd/lnd-debug --rpclisten=localhost:100"+port+" --listen=localhost:201"\
                   +port+" --restlisten=localhost:80"+port+" --lnddir=lnd " \
    "--debuglevel=info --bitcoin.simnet --bitcoin.active --bitcoin.node=btcd --btcd.rpcuser=kek --btcd.rpcpass=kek --no-macaroons"

    print command_line
    args = shlex.split(command_line)
    processes.append(Popen(args))

time.sleep(10)

for i in range(n):
    os.chdir("/Users/thanh_nc/lnd/simnet/" + str(i))
    print(directory + str(i) + '/lnd/tls.cert')
    cert = open(directory + str(i) + '/lnd/tls.cert').read()
    creds = grpc.ssl_channel_credentials(cert)
    port = str(i) if i >= 10 else '0' + str(i)
    channel = grpc.secure_channel('localhost:100' + port, creds)
    stub = lnrpc.WalletUnlockerStub(channel)
    request = ln.GenSeedRequest(
            aezeed_passphrase=None,
            seed_entropy=None,
        )
    response = stub.GenSeed(request)
    request = ln.InitWalletRequest(
        wallet_password=b'123456789',
        cipher_seed_mnemonic=response.cipher_seed_mnemonic,
        aezeed_passphrase=None
    )
    response = stub.InitWallet(request)
    print(response)
    time.sleep(10)

time.sleep(10)

for i in range(n):
    os.chdir("/Users/thanh_nc/lnd/simnet/" + str(i))
    print(directory + str(i) + '/lnd/tls.cert')
    cert = open(directory + str(i) + '/lnd/tls.cert').read()
    creds = grpc.ssl_channel_credentials(cert)
    port = str(i) if i >= 10 else '0' + str(i)
    channel = grpc.secure_channel('localhost:100' + port, creds)
    stub = lnrpc.LightningStub(channel)
    request = ln.NewAddressRequest(
        type=1
    )
    response = stub.NewAddress(request)
    print response


    btcd.terminate()
    command_line = "/Users/thanh_nc/go/bin/btcd --txindex --simnet --maxpeers=100 --rpcmaxwebsockets=100 --rpcuser=kek --rpcpass=kek --miningaddr=" + response.address
    print command_line
    args = shlex.split(command_line)
    btcd = Popen(args)
    time.sleep(10)
    command_line = "/Users/thanh_nc/go/bin/btcctl --simnet --rpcuser=kek --rpcpass=kek generate 200"
    print command_line
    args = shlex.split(command_line)
    call(args)
    time.sleep(10)
time.sleep(5)




for i in range(n):
    os.chdir("/Users/thanh_nc/lnd/simnet/" + str(i))
    print(directory + str(i) + '/lnd/tls.cert')
    cert = open(directory + str(i) + '/lnd/tls.cert').read()
    creds = grpc.ssl_channel_credentials(cert)
    port = str(i) if i >= 10 else '0' + str(i)
    channel = grpc.secure_channel('localhost:100' + port, creds)
    stub = lnrpc.LightningStub(channel)
    request = ln.GetInfoRequest()
    response = stub.GetInfo(request)
    address.append(response.identity_pubkey)
    print response


for i in range(n):
    os.chdir("/Users/thanh_nc/lnd/simnet/" + str(i))
    print(directory + str(i) + '/lnd/tls.cert')
    cert = open(directory + str(i) + '/lnd/tls.cert').read()
    creds = grpc.ssl_channel_credentials(cert)
    port = str(i) if i >= 10 else '0' + str(i)
    channel = grpc.secure_channel('localhost:100' + port, creds)
    stub = lnrpc.LightningStub(channel)

    for j in data[i].split():
        print j
        port2 = str(j) if int(j) >= 10 else '0' + str(j)
        print port2
        request = ln.ConnectPeerRequest(
            addr=ln.LightningAddress(pubkey=address[int(j)],
                                     host='localhost:201' + port2)
        )
        print address[int(j)] + '@localhost:201' + port2
        response = stub.ConnectPeer(request)
        print response
        print str.encode(str(address[int(j)]))
        time.sleep(10)

        print address[int(j)]
        request = ln.OpenChannelRequest(
            node_pubkey=str(address[int(j)]),
            node_pubkey_string=str(address[int(j)]),
            local_funding_amount=5000000,
            push_sat=3000000
        )
        response = stub.OpenChannelSync(request)
        # Do something
        print response
        command_line = "/Users/thanh_nc/go/bin/btcctl --simnet --rpcuser=kek --rpcpass=kek generate 4"
        print command_line
        args = shlex.split(command_line)
        call(args)
        time.sleep(10)


while True:
    btcd.poll()


