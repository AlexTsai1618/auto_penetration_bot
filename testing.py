import subprocess

print '\nread:'
proc = subprocess.Popen(['echo', '"to stdout"'], 
                        stdout=subprocess.PIPE,
                        )
stdout_value = proc.communicate()[0]
print '\tstdout:', repr(stdout_value)