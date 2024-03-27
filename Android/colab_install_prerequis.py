import os,subprocess

error_log = "install.log"
python_pip_install = ["pip","install","Buildozer",";","pip","install","cython"]
shell_install =[
  "python3-pip",
  "build-essential",
  "git",
  "python3",
  "python3-dev",
  "ffmpeg",
  "libsdl2-dev",
  "libsdl2-image-dev",
  "libsdl2-mixer-dev",
  "libsdl2-ttf-dev",
  "libportmidi-dev",
  "libswscale-dev",
  "libavformat-dev",
  "libavcodec-dev",
  "zlib1g-dev",
  "libgstreamer1.0",
  "gstreamer1.0-plugins-base",
  "gstreamer1.0-plugins-good",
  "libsqlite3-dev",
  "sqlite3",
  "bzip2",
  "libbz2-dev",
  "libssl-dev",
  "openssl",
  "libgdbm-dev",
  "libgdbm-compat-dev",
  "liblzma-dev",
  "libreadline-dev",
  "libncursesw5-dev",
  "libffi-dev",
  "uuid-dev",
  "libffi7",
  "libtool"
]

update_apt_get = ["sudo","apt","update","&&","sudo","apt","upgrade","-y"]

def install_multiple_shell_libraries(lib):
    install = ["sudo","apt-get","install","-y",lib]
    try:
      subprocess.run(install, shell=True, check=True)
    except subprocess.CalledProcessError as e:
      print (e)
      pass

print ("""
################## Debut d'installation des pre-requis pour le build android ###################
            -------------- Mise a jour de l'apt ---------------
""")

try:
  subprocess.run(update_apt_get, shell=True, check=True)
except subprocess.CalledProcessError as e:
  print (e)
  pass

print ("-------------- Installation des librairies linux nécessaire ---------------")
threads = []
for lib in shell_install:
  t = threading.Thread(target=install_multiple_shell_libraries, args=(lib,))
  t.start()
  threads.append(t)
for thread in threads:
  thread.join()

print ("-------------- Installation Buildozer et cython ---------------")
try:
  subprocess.run(python_pip_install, shell=True, check=True)
except subprocess.CalledProcessError as e:
  print (e)
  pass

print ("------------- Installation du jdk nécessaire ----------------")
jdk_install = ["sudo","apt-get","install","openjdk-17-jre-headless","-qq"]
try:
  subprocess.run(jdk_install, shell=True, check=True)
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
  subprocess.run(["update-alternatives","--set","java","/usr/lib/jvm/java-17-openjdk-amd64/bin/java",";","java","-version"], shell=True, check=True)
except subprocess.CalledProcessError as e:
  print (e)
  pass

print ("########## Fin du script ##############")














       
