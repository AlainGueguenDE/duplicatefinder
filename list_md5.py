import tkinter as tk
from os import walk,stat,environ
import os
import time
import datetime
import hashlib
import pandas as pd
import logging
import sys
from pathlib import Path

LOGLEVEL = environ.get('LOGLEVEL', 'DEBUG')  #.upper()

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=LOGLEVEL)

ts= time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


def file_as_bytes(file):
    with file:
        return file.read()

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def findDuplicate(filename):
    """
       take a file and find double entries from a triplet of 3 first columns
       save a list of these duplicate in a csv file
       input : filename of the initial csv
               save the result in a new csv file with a suffixe "_filtered"

    """


    lstofmd5=open(filename,'r')
    filename1=filename.split('.csv')[0]
    resfilename="%s_filtered.csv"%filename1
    filelstofdoublon=open(resfilename,'w')
    colname=[]
    colsize=[]
    colmd5=[]
    for line in lstofmd5:
        tabtmp=line.split("|")
        colname.append(tabtmp[0])
        colsize.append(tabtmp[1])
        colmd5 .append(tabtmp[2])
    sortedhash = colmd5.copy()
    sortedhash.sort()

    new_list = sorted(set(sortedhash))
    dup_list =[]
    for i in range(len(new_list)):
        if (colmd5.count(new_list[i]) > 1 ):
            dup_list.append(new_list[i]) #store the duplicated md5 ...
    #must loop over the original list  and everytime md5 is in the dup list copy the full line of 3 parameters
    listofdoublon=[]
    j=0
    e=[]
    for k in range(len(colname)):
        if colmd5[k] in dup_list:
            strtmp = "%s|%s|%s"%(colname[k], colsize[k], colmd5[k] )
            e.append([colname[k], colsize[k], colmd5[k]])
            listofdoublon.append(strtmp)
            filelstofdoublon.write(strtmp)
    filelstofdoublon.close()
    #order the list on md5 #
    f= sorted(e, key = lambda x: x[2])
    resfilenamesorted="%s_filtered_sorted.csv"%filename1
    filelstofdoublonsorted=open(resfilenamesorted,'w')
    for i in range(len(f)):
        strtmp = "%s|%s|%s"%(f[i][0], f[i][1], f[i][2])
        filelstofdoublonsorted.write(strtmp)
    filelstofdoublonsorted.close()


def creatDFmd5(foldertosearch,resultfile):
    """
      take a path as a strong and walk through
       for all files compute the MD5 and store it with the size, path and name name in a dataframe.
       the dataframe is then saevd in a file , passed as the second parameter

       input
        foldertosearch: string of the full path of the folder to go through
        resultfile: string of the name of the file to store the result.
            it call also a function to filter the dataframe and save only the duplicate entries ( duplicate on md5/ size)
       return the number of file  seen

       TODO : add some security and safeguard on the existence of the folder to read , the succes to save the csv files .

    """
    df = pd.DataFrame(columns=['filename', 'filepath','size','hashmd5'])
    starttime = time.time()
    compteurlocal=0
    for (i,j,k )in os.walk(foldertosearch):
        for filname in k:
           compteurlocal+=1
           cmdline= "%s/%s"%(i,filname)
           statinfo = os.stat(cmdline)

           #mainstring= ("%s/%s | %s | %s \n"%(i,filname,statinfo.st_size,hashlib.md5(file_as_bytes(open(cmdline, 'rb'))).hexdigest()))
           new_row={'filename':i, 'filepath':"%s/%s"%(i,filname),'size':statinfo.st_size,'hashmd5':hashlib.md5(file_as_bytes(open(cmdline, 'rb'))).hexdigest()}
           df.loc[compteurlocal] = new_row

    df.to_csv( resultfile , encoding='utf-8', index=False)
    extractedpath=os.path.dirname(resultfile)
    prefix=Path(resultfile).stem
    nameforduplicate=os.path.join(extractedpath,"%s_duplicate.csv"%prefix)
    flagduplicateindf(resultfile,nameforduplicate )#'duplicated_.csv')
    return compteurlocal

def creatDFmd5LST(foldertosearchLST,resultfile):
    """
      take a list of folder path and walk through all of them
       for all files compute the MD5 and store it with the size, path and name name in a dataframe.
       the dataframe is then saevd in a file , passed as the second parameter

       input
        foldertosearch: string of the full path of the folder to go through
        resultfile: string of the name of the file to store the result.
            it call also a function to filter the dataframe and save only the duplicate entries ( duplicate on md5/ size)
       return the number of file  seen

       TODO : add some security and safeguard on the existence of the folder to read , the succes to save the csv files .

    """

    df = pd.DataFrame(columns=['filename', 'filepath','size','hashmd5'])
    starttime = time.time()
    compteurlocal=0
    for foldertosearch in foldertosearchLST:
        if len(foldertosearch) >0:
            print ("start in ",foldertosearch)
            for (i,j,k )in os.walk(foldertosearch):
                for filname in k:
                    compteurlocal+=1
                    cmdline= "%s/%s"%(i,filname)
                    statinfo = os.stat(cmdline)

                    #mainstring= ("%s/%s | %s | %s \n"%(i,filname,statinfo.st_size,hashlib.md5(file_as_bytes(open(cmdline, 'rb'))).hexdigest()))
                    new_row={'filename': filname, 'filepath':"%s/%s"%(i,filname),'size':statinfo.st_size,'hashmd5':hashlib.md5(file_as_bytes(open(cmdline, 'rb'))).hexdigest()}
                    df.loc[compteurlocal] = new_row

    df.to_csv( resultfile , encoding='utf-8', index=False)
    extractedpath=os.path.dirname(resultfile)
    #=os.path.basename(resultfile)
    prefix=Path(resultfile).stem
    nameforduplicate=os.path.join(extractedpath,"%s_duplicate.csv"%prefix)
    df_dupli=flagduplicateindf(resultfile,nameforduplicate )#'duplicated_.csv')
    return df, df_dupli , compteurlocal

def creatDFmd5LST_feedback(foldertosearchLST,resultfile,maintk):
    """
      take a list of folder path and walk through all of them
       for all files compute the MD5 and store it with the size, path and name name in a dataframe.
       the dataframe is then saevd in a file , passed as the second parameter
       this  function send feedback to the main window (defined in  gui_V0.2 ) about the evolution of the process.

       input
        foldertosearch: string of the full path of the folder to go through
        resultfile: string of the name of the file to store the result.
            it call also a function to filter the dataframe and save only the duplicate entries ( duplicate on md5/ size)
       return the number of file  seen

       TODO : add some security and safeguard on the existence of the folder to read , the succes to save the csv files .
    """
    df = pd.DataFrame(columns=['filename', 'filepath','size','hashmd5'])
    starttime = time.time()
    compteurlocal=0
    maintk.text_box.insert("1.0", "%s\n"%resultfile)
    print (type(maintk))
    maintk.text_box.update_idletasks()
    for foldertosearch in foldertosearchLST:
        if len(foldertosearch) >0:
            print ("start in ",foldertosearch)
            for (i,j,k )in os.walk(foldertosearch):
                for filname in k:
                    compteurlocal+=1
                    if compteurlocal%100==0:
                        maintk.text_box.insert("1.0", "%s\n"%compteurlocal)
                        maintk.text_box.update_idletasks()
                        #    break
                    cmdline= "%s/%s"%(i,filname)
                    if os.path.exists(cmdline):
                        statinfo = os.stat(cmdline)

                    #mainstring= ("%s/%s | %s | %s \n"%(i,filname,statinfo.st_size,hashlib.md5(file_as_bytes(open(cmdline, 'rb'))).hexdigest()))
                    new_row={'filename': filname, 'filepath':"%s/%s"%(i,filname),'size':statinfo.st_size,'hashmd5':hashlib.md5(file_as_bytes(open(cmdline, 'rb'))).hexdigest()}
                    df.loc[compteurlocal] = new_row

    df.to_csv( resultfile , encoding='utf-8', index=False)
    extractedpath=os.path.dirname(resultfile)
    prefix=Path(resultfile).stem
    nameforduplicate=os.path.join(extractedpath,"%s_duplicate.csv"%prefix)
    df_dupli=flagduplicateindf(resultfile,nameforduplicate )#'duplicated_.csv')
    return df, df_dupli , compteurlocal

def flagduplicateindf(dfin,dfoutName):
    """
     take a dataframe with must contains 2 columns 'size','hashmd5' keep only duplicated lines on this doublet
     it it save the doublet dataframe as csv , using the second paramerr as filename
     it return the  dataframe of the doublet
     input :
         dfin      original dataframe
         dfoutName filename to save the filtered datarame
     output:
         the dataframe of the douvblet

     TODO: add some safeguard on existence ofcontent  the dataframe (columns and emptyness)
    """
    df = pd.read_csv(dfin)
    df2=df.duplicated(subset=['size','hashmd5'],keep=False)
    df=df.loc[df2]
    df.to_csv( dfoutName)
    return df

def main(args):
    function ="Main"
    logger = logging.getLogger(__name__)
    logger.debug("in %s:  "%function)
    status=0
    statusreffile=0
    folderin=''
    for arg in args:
        if "folderin" in arg:
            folderin=arg.split('=')[1]

            if ',' in folderin:
                folderin=folderin.split(',')
            else:
                folderin=[folderin]
            statusfold=1
        if "resultfile" in arg:
            reftaskfile =arg.split('=')[1]
            statusreffile+=1

    if statusfold !=1 :
        print ( "error missing picture main folder, must be given as folderin=<start path for the search>")
        return

    if statusreffile !=1 :
        print ( "error missing result csv file, must be given as resultfile=<full or relative path to the result file >")
        return

    if os.path.isdir(folderin):
        print ("folder ok ")
    else:
        print ("input folder %s  does not exist check and launch again"%folderin)
        return

    if os.path.isfile(reftaskfile):
        print ("Warning reference file already exist")
    else:
        print ("result file %s  does not exist will be created"%reftaskfile)
        #return

    endtime=time.time()
    compteurlocal= creatDFmd5(folderin,reftaskfile)
    #listtotalemd5size.close()
    print ("checked %s files"%compteurlocal)



if __name__ == "__main__":
    main(sys.argv)
    print("command line mode finished ")