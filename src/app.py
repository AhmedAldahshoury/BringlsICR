import os, sys
from flask import Flask, render_template, request
from shutil import copyfile
from flask import jsonify

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/", methods=['POST'])
def upload():
    print("----------------------------Uploading Started--------------------------------")

    target = os.path.join(APP_ROOT, '../dataset/raw')
    uploadDir = os.path.join(APP_ROOT, 'static/uploadsTemp')

    if not os.path.isdir(target):
        os.mkdir(target)

    print(str(len(request.files.getlist("file"))) + " images selected ")
    counter = 1
    for file in request.files.getlist("file"):
        filename = file.filename
        saveDes = "/".join([target, filename])
        uploadDes = "/".join([uploadDir, filename])
        file.save(saveDes)
        copyfile(saveDes, uploadDes)
        filename = filename.replace('.png', '')
        print(str(counter) + " -- (" + filename + ".png) uploaded")
        counter += 1

    print("Images uploaded successfully")
    print("---------------------------Uploading Ended---------------------------------")
    return render_template("upload.html")


@app.route("/recognize", methods=['POST'])
def recognize():
    threshold = 10
    f = open('../model/wordCharList.txt', 'w+')

    folders = os.listdir('../dataset/segmented')
    folders = [folder for folder in folders if '.DS_Store' not in folder]
    for folder in folders:
        files = os.listdir('../dataset/segmented/' + str(folder))
        files = [file for file in files if '.DS_Store' not in file]
        if len(files) > threshold:
            f.write("%s\n" % folder)
    f.close()

    images = os.listdir('static/gallery')
    images = [image for image in images if '.DS_Store' not in image]

    for image in images:
        os.unlink(os.path.join(APP_ROOT, 'static/gallery/' + image))

    print("---------------------------Recognition Started---------------------------------")
    folderDir = os.path.join(APP_ROOT, 'static/uploadsTemp')
    images = os.listdir('static/uploadsTemp')
    images = [image for image in images if '.DS_Store' not in image]

    if len(images) > 0:

        if images[0] == ".DS_Store":
            del images[0]
        for file in images:
            print("Segmenting: " + str(file))
            filename = str(file)
            filename = filename.replace('.png', '')
            call = str('python segmentation.py ' + str(filename) + " 1")
            print("calling: " + call)
            os.system(call)
            fileDir = os.path.join(folderDir, str(file))
            os.unlink(fileDir)

        if not os.path.isdir("../dataset/recognized"):
            os.mkdir("../dataset/recognized")
        images = os.listdir('static/gallery')
        if images and images[0] == ".DS_Store":
            del images[0]
        images = ['gallery/' + file for file in images]
        counter = 1
        f = open('../dataset/recognized/recognized.txt', 'w+')
        f.write("")
        f.close()
        if images:
            images.sort()
            print(str(images))
            for image in images:
                print("---------------------------Recognizing: " + str(counter) + "/" + str(
                    len(images)) + "---------------------------------")
                call = str('python main.py --wordbeamsearch')
                srcDir = os.path.join(APP_ROOT, 'static/' + image)
                saveDir = os.path.join(APP_ROOT, '../dataset/test.png')
                copyfile(srcDir, saveDir)
                os.system(call)
                os.unlink(saveDir)
                counter += 1

        print("---------------------------Recognition Ended---------------------------------")

    images = os.listdir('static/gallery')
    for image in images:
        os.unlink(os.path.join(APP_ROOT, 'static/gallery/' + image))

    return render_template('upload.html')


@app.route("/segment", methods=['POST', 'GET'])
def segment():
    print("---------------------------Segmentation Started---------------------------------")
    folderDir = os.path.join(APP_ROOT, 'static/uploadsTemp')
    images = os.listdir('static/uploadsTemp')
    images = [image for image in images if '.DS_Store' not in image]
    if images:
        if images[0] == ".DS_Store":
            del images[0]
        for file in images:
            print("Segmenting: " + str(file))
            filename = str(file)
            filename = filename.replace('.png', '')
            call = str('python segmentation.py ' + str(filename) + " 1")
            print("calling: " + call)
            os.system(call)
            fileDir = os.path.join(folderDir, str(file))
            os.unlink(fileDir)

        print("---------------------------Segmentation Ended---------------------------------")

        images = os.listdir('static/gallery')
        images = [image for image in images if '.DS_Store' not in image]
        if images and images[0] == ".DS_Store":
            del images[0]
        images = ['gallery/' + file for file in images]

        if images:
            return render_template('gallery.html', images=images)
        else:
            return render_template('gallery.html')
    else:
        f = open('output.txt', 'w+')
        f.write("")
        f.close()
        return render_template('train.html')


@app.route("/augment", methods=['POST'])
def augment():
    f = open('output.txt', 'w+')
    f.write("")
    f.close()
    print("---------------------------Augmentation Started---------------------------------")
    files = os.listdir('../dataset/segmented')
    files = [file for file in files if '.DS_Store' not in file]
    if files:
        if files[0] == ".DS_Store":
            del files[0]
        counter = 0
        for file in files:
            os.system('python dataGenerator.py ' + file + ' | tee -a')
            # for multithreading, use the line below
            # command1 = subprocess.Popen(['python', 'dataGenerator.py', file, '| tee -a output.txt'])
            counter += 1
            print("Augmenting (" + str(counter) + ") files")
        print("loading...")
        print("---------------------------Augmentation Ended---------------------------------")

    return render_template("train.html")


@app.route("/generateDB", methods=['POST'])
def generateDB():
    print("---------------------------Generating DB Starting---------------------------------")
    os.system('python dbwriter.py')
    count = len(open("../dataset/words.txt").readlines())
    print("Total of (" + str(count) + ") images in the database")

    print("---------------------------Generating DB Ended---------------------------------")

    return render_template("train.html")


@app.route("/train", methods=['POST'])
def train():
    print("---------------------------Training Started---------------------------------")
    os.system('python main.py --train')
    print("---------------------------Training Ended---------------------------------")
    return render_template("train.html")


@app.route("/remove", methods=['POST'])
def remove():
    target = os.path.join(APP_ROOT, "static/" + request.form.get('image'))
    os.remove(target)
    print("Image : (" + request.form.get('image') + ") is DELETED !!")
    images = os.listdir('static/gallery')
    if images[0] == ".DS_Store":
        del images[0]
    images = ['gallery/' + file for file in images]
    if (len(images) > 1):
        return render_template('gallery.html', images=images)
    else:
        return render_template('gallery.html')


@app.route("/save", methods=['POST'])
def save():
    target = os.path.join(APP_ROOT, "static/" + request.form.get('image'))
    src = os.path.join(APP_ROOT, "static/" + request.form.get('image'))
    root = APP_ROOT.replace('/src', '')
    dest = request.form.get('image').replace('gallery', '')
    print("dest:" + dest)
    dst2 = str(root + "/dataset/segmented/" + request.form.get('targetText'))
    if not os.path.exists(dst2):
        os.makedirs(dst2)
    files = os.listdir(dst2)
    counter = len(files)
    dst = str(
        root + "/dataset/segmented/" + request.form.get('targetText') + "/" + request.form.get(
            'targetText') + "_" + str(counter) + ".png")
    copyfile(src, dst)
    print("Image: (" + request.form.get('image') + ") is labeled as: (" + request.form.get('targetText') + ")")
    os.remove(target)
    images = os.listdir('static/gallery')
    if len(images) > 0:
        if images[0] == ".DS_Store":
            del images[0]
        images = ['gallery/' + file for file in images]
        return render_template('gallery.html', images=images)
    return render_template('gallery.html')


@app.route("/deleteAll", methods=['POST'])
def deleteAll():
    print("---------------------------Deleting All Started---------------------------------")
    folderDir = os.path.join(APP_ROOT, 'static/gallery')
    images = os.listdir('static/gallery')
    images = [image for image in images if '.DS_Store' not in image]
    if len(images) > 0:
        if images[0] == ".DS_Store":
            del images[0]
        for file in images:
            print("Deleteing : " + str(file))
            fileDir = os.path.join(folderDir, str(file))
            os.unlink(fileDir)
        images = os.listdir('static/gallery')
        if len(images) > 0:
            if images[0] == ".DS_Store":
                del images[0]
            images = ['gallery/' + file for file in images]
            return render_template('gallery.html', images=images)
    print("---------------------------Deleting All Ended---------------------------------")
    return render_template('gallery.html')


@app.route("/terminal", methods=['GET', 'POST'])
def terminal():
    render_template('train.html')
    outputFile = 'output.txt'
    fr = open(outputFile, "r")
    data_list = fr.readlines()
    for idx in range(len(data_list)):
        data_list[idx] = data_list[idx].replace('<br />', '')
        data_list[idx] = data_list[idx].replace(',', ' ')
        data_list[idx] = data_list[idx] + "<br />"
        data_list[idx] = data_list[idx].replace('<br />', '<br />')
    if (file_len(outputFile) > 10):
        del data_list[0:1]
        fw = open(outputFile, 'w+')
        fw.writelines(data_list)
        fw.close()
    return jsonify(data_list)


@app.route("/targets", methods=['POST'])
def targetText():
    images = os.listdir('static/gallery')
    images = [image for image in images if '.DS_Store' not in image]
    images = ['gallery/' + file for file in images]
    return render_template('gallery.html', images=images)


def file_len(fname):
    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


if __name__ == "__main__":
    app.run(port=4555, debug=True, threaded=True)
