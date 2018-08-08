import os
from subprocess import Popen, PIPE, STDOUT, run
import shlex
import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc

os.chdir("/Users/thanh_nc/lnd/simnet")
processes = []
timeout = 0.1
for i in range(2):
    # subprocess.run(["mkdir",str(i)])
    command_line = "/Users/thanh_nc/gocode/bin/lnd --help"
    args = shlex.split(command_line)
    run(args, stdout=PIPE)
    os.chdir("/Users/thanh_nc/lnd/simnet/" + str(i))
    # command_line = "/Users/thanh_nc/gocode/bin/lnd --rpclisten=localhost:1000"+str(i)+" --listen=localhost:1001"+str(i)\
    #                +" --restlisten=localhost:800"+str(i)+" --datadir=data --logdir=log --debuglevel=info --bitcoin.simnet " \
    #                                                      "--bitcoin.active --bitcoin.node=btcd --btcd.rpcuser=kek --btcd.rpcpass=kek --no-macaroons"
    # print(command_line)
    # args = shlex.split(command_line)
    
    # processes.append(Popen(args))
    command_line = "/Users/thanh_nc/gocode/bin/lncli --rpcserver=localhost:1000"+str(i)+" --macaroonpath=data/admin.macaroon create"
    args = shlex.split(command_line)
    print(command_line)
    proc = Popen([command_line], stdin=PIPE, stdout=PIPE, shell=True)
    print(proc.stdout.read().decode())
    # processes.append(proc)
    grep_stdout = proc.communicate(b'123456789\n123456789\nn\nn\n\n\n\n\n')



    # a = proc.stdin.write(b'123456789\n123456789\n n\n\n\n')
    # proc.stdin.close()
    # proc.wait()
    # print(a)
    print(grep_stdout)
    # print(grep_stdout[0].decode())
    #
    while processes:
        # remove finished processes from the list (O(N**2))
        for p in processes[:]:
            if p.poll() is not None:  # process ended
                print("aaaaa")
                # print(p.stdout.read().decode(), end='')  # read the rest
                # p.stdout.close()
                processes.remove(p)

        # wait until there is something to read
        # rlist = select([p.stdout for p in processes], [], [], timeout)[0]

        # read a line from each process that has output ready
        # for f in rlist:
        #     print(f.readline(), end='')  # NOTE: it can block

    break

