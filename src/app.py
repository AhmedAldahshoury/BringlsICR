import os
import sys
from flask import Flask, render_template, request
from shutil import copyfile
from flask import jsonify
from pathlib import Path

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)
app = Flask(__name__)


ROOT_PATH = Path(__file__).resolve().parents[1]
DATASET_PATH = os.path.join(ROOT_PATH, 'dataset')
GALLERY_PATH = os.path.join(ROOT_PATH, 'src', 'static', 'gallery')
TEMP_UPLOADS_PATH = os.path.join(ROOT_PATH, 'src', 'static', 'uploadsTemp')
MIN_INSTANCES_TO_TRAIN = 10


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/", methods=['POST'])
def upload():
    print("----------------------------Uploading Started--------------------------------")

    target = os.path.join(DATASET_PATH, 'raw')
    if not os.path.isdir(target):
        os.mkdir(target)

    if not os.path.isdir(TEMP_UPLOADS_PATH):
        os.mkdir(TEMP_UPLOADS_PATH)

    print('{} images selected'.format(len(request.files.getlist("file"))))
    counter = 1
    for file in request.files.getlist("file"):
        filename = file.filename
        save_des = os.path.join(target, filename)
        upload_des = os.path.join(TEMP_UPLOADS_PATH, filename)
        file.save(save_des)
        copyfile(save_des, upload_des)
        print('{} -- ({} uploaded)'.format(counter, filename))
        counter += 1

    print("Images uploaded successfully")
    print("---------------------------Uploading Ended---------------------------------")
    return render_template("upload.html")


@app.route("/recognize", methods=['POST'])
def recognize():
    f = open('../model/wordCharList.txt', 'w+')

    folders = os.listdir(os.path.join(DATASET_PATH, 'segmented'))
    folders = [folder for folder in folders if '.DS_Store' not in folder]
    for folder in folders:
        files = os.listdir(os.path.join(DATASET_PATH, 'segmented', str(folder)))
        files = [file for file in files if '.DS_Store' not in file]
        if len(files) > MIN_INSTANCES_TO_TRAIN:
            f.write("%s\n" % folder)
    f.close()

    images = os.listdir(GALLERY_PATH)
    images = [image for image in images if '.DS_Store' not in image]

    for image in images:
        os.unlink(os.path.join(GALLERY_PATH, image))

    print("---------------------------Recognition Started---------------------------------")

    images = os.listdir(TEMP_UPLOADS_PATH)
    images = [image for image in images if '.DS_Store' not in image]

    if images:
        for file in images:
            print("Segmenting: {}".format(file))
            filename = str(file).replace('.png', '')
            call = str('python segmentation.py {} 1'.format(filename))
            print("calling: {}".format(call))
            os.system(call)
            fileDir = os.path.join(TEMP_UPLOADS_PATH, str(file))
            os.unlink(fileDir)

        if not os.path.isdir(os.path.join(DATASET_PATH, 'recognized')):
            os.mkdir(os.path.join(DATASET_PATH, 'recognized'))
        images = os.listdir(GALLERY_PATH)
        images = [image for image in images if '.DS_Store' not in image]
        images = ['gallery/' + file for file in images]
        counter = 1
        f = open(os.path.join(DATASET_PATH, 'recognized', 'recognized.txt'), 'w+')
        f.write("")
        f.close()
        if images:
            images.sort()
        print(str(images))
        for image in images:
            print("--------------------------- "
                  "Recognizing: {}/{}"
                  " ---------------------------------".format(counter, len(images)))

            call = str('python main.py --wordbeamsearch')
            srcDir = os.path.join(ROOT_PATH, 'src', 'static', image)
            saveDir = os.path.join(DATASET_PATH, 'test.png')
            copyfile(srcDir, saveDir)
            os.system(call)
            os.unlink(saveDir)
            counter += 1

        print("---------------------------Recognition Ended---------------------------------")

        images = os.listdir(GALLERY_PATH)
        for image in images:
            os.unlink(os.path.join(GALLERY_PATH, image))

    return render_template('upload.html')


@app.route("/segment", methods=['POST', 'GET'])
def segment():
    print("---------------------------Segmentation Started---------------------------------")
    folderDir = TEMP_UPLOADS_PATH
    if not os.path.isdir(folderDir):
        os.mkdir(folderDir)
    images = os.listdir(folderDir)
    images = [image for image in images if '.DS_Store' not in image]
    if images:
        for image in images:
            print("Segmenting: {}".format(image))
            filename = str(image).replace('.png', '')
            call = str('python segmentation.py {} 1'.format(filename))
            print("calling: {}".format(call))
            os.system(call)
            image_dir = os.path.join(folderDir, str(image))
            os.unlink(image_dir)

        print("---------------------------Segmentation Ended---------------------------------")
        if not os.path.isdir(GALLERY_PATH):
            os.mkdir(GALLERY_PATH)
        images = os.listdir(GALLERY_PATH)
        images = [os.path.join('gallery', image) for image in images if '.DS_Store' not in image]
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
    files = os.listdir(os.path.join(DATASET_PATH, 'segmented'))
    files = [file for file in files if '.DS_Store' not in file]
    if files:
        counter = 0
        for file in files:
            os.system('python dataGenerator.py ' + file + ' | tee -a')
            # for multithreading, use the line below
            # command1 = subprocess.Popen(['python', 'dataGenerator.py', file, '| tee -a output.txt'])
            counter += 1
            print("Augmenting ({}) files".format(counter))
        print("loading...")

    print("---------------------------Augmentation Ended---------------------------------")
    return render_template("train.html")


@app.route("/generateDB", methods=['POST'])
def generateDB():
    print("---------------------------Generating DB Starting---------------------------------")
    os.system('python dbwriter.py')
    count = len(open("dataset','words.txt").readlines())
    print("Total of ({}) images in the database".format(count))

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
    target = os.path.join(ROOT_PATH, 'src', 'static', request.form.get('image'))
    os.remove(target)
    print('Image : ({}) is DELETED!!'.format(request.form.get('image')))
    images = os.listdir(os.path.join(GALLERY_PATH))
    images = [os.path.join('gallery', image) for image in images if '.DS_Store' not in image]
    if images:
        return render_template('gallery.html', images=images)
    else:
        return render_template('gallery.html')


@app.route("/save", methods=['POST'])
def save():
    target = os.path.join(ROOT_PATH, 'src', 'static', request.form.get('image'))
    src = os.path.join(ROOT_PATH, 'src', 'static', request.form.get('image'))
    dest = request.form.get('image').replace('gallery', '')
    print("destination:" + dest)
    dst2 = os.path.join(DATASET_PATH, 'segmented' + request.form.get('targetText'))
    if not os.path.exists(dst2):
        os.makedirs(dst2)
    files = os.listdir(dst2)
    counter = len(files)
    dst = os.path.join(DATASET_PATH, 'segmented', request.form.get('targetText'), request.form.get(
        'targetText')) + "_" + str(counter) + ".png"
    copyfile(src, dst)
    print("Image: ({}) is labeled as: ({})".format(request.form.get('image'), request.form.get('targetText')))
    os.remove(target)
    images = os.listdir(GALLERY_PATH)
    if images:
        images = [os.path.join('gallery', image) for image in images if '.DS_Store' not in image]
        return render_template('gallery.html', images=images)
    return render_template('gallery.html')


@app.route("/deleteAll", methods=['POST'])
def deleteAll():
    print("---------------------------Deleting All Started---------------------------------")
    if not os.path.isdir(GALLERY_PATH):
        os.mkdir(GALLERY_PATH)
    images = os.listdir(GALLERY_PATH)
    images = [image for image in images if '.DS_Store' not in image]
    if images:
        for file in images:
            print("Deleteing: {}".format(file))
            file_dir = os.path.join(GALLERY_PATH, file)
            os.unlink(file_dir)
        images = os.listdir(GALLERY_PATH)
        if images:
            images = [os.path.join('gallery', image) for image in images]
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
    if file_len(outputFile) > 10:
        del data_list[0:1]
        fw = open(outputFile, 'w+')
        fw.writelines(data_list)
        fw.close()
    return jsonify(data_list)


@app.route("/targets", methods=['POST'])
def targetText():
    images = os.listdir(GALLERY_PATH)
    images = [os.path.join('gallery', image) for image in images if '.DS_Store' not in image]
    return render_template('gallery.html', images=images)


def file_len(fname):
    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


if __name__ == "__main__":
    app.run(port=4555, debug=True, threaded=True)
