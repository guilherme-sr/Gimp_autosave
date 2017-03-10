import tempfile, os
from time import *
from gimpfu import *


def autosave():
    backupInterval = 2*60

    backupFiles = {}
    print "Autosave activated"

    while 1:
        sleep(backupInterval)

        print ctime(time())

        curImages = {}
        for k in gimp.image_list():
            curImages[k.ID] = k

        curIDs = curImages.keys()
        oldIDs = backupFiles.keys()

        newIDs = [x for x in curIDs if x not in oldIDs];
        delIDs = [x for x in oldIDs if x not in curIDs];

        # create (empty) backup files for new images
        for id in newIDs:
            prefix = 'gimpbackup-ID' + str(id) + '-'
            fn = tempfile.mkstemp(prefix = prefix, suffix = '.xcf')
            os.close(fn[0])
            backupFiles[id] = fn[1]

        # remove closed images' backups
        for id in delIDs:
            filename = backupFiles[id]
            del(backupFiles[id])
            try:
                os.remove(filename)
            except:
                print "ERROR: ", sys.exc_info()[0]

        # backup images
        for id, filename in backupFiles.iteritems():
            img = curImages[id]
            try:
                print "saving " + img.name + '-' + str(id) + ' to ' + filename
                pdb.gimp_xcf_save(1, img, img.active_drawable, filename, 
filename)
            except:
                print "ERROR: ", sys.exc_info()[0]




register(
        "autosave",
        "Autosave dirty hack",
        "Periodically saves all opened images to a temp directory",
        "public domain",
        "public domain",
        "2009",
        "<Toolbox>/File/Activate Autosave",
        "RGB*, GRAY*",
        [],
        [],
        autosave)

main()

