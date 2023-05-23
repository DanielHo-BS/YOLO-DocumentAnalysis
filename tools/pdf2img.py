from PIL import Image
import os
import fitz

def pdf2imgs(pdf_src):
    zoom_x, zoom_y= 2.0, 2.0
    mat=fitz.Matrix(zoom_x,zoom_y)
    if pdf_src.find('/')!=-1:
        filename=pdf_src.split('/')[-2]+'_'+pdf_src.split('/')[-1]
    else:
        filename=pdf_src.split('\\')[-2]+'_'+pdf_src.split('\\')[-1]
    foldername=filename.split(".")[0]
    if filename.split(".")[-1] != "pdf":
        print("Skip the file: "+filename)
        return None
    #if not os.path.exists('./img'):
    #    os.makedirs('./img')
    if not os.path.exists('./img/'+foldername):
        os.makedirs('./img/'+foldername)
    doc=fitz.open(pdf_src)
    output_ls = []
    for page in doc:
        pix=page.get_pixmap(matrix=mat)
        j=str(page.number+1).rjust(3,'0')
        output_ls.append("./img/%s/page_%s.png" % (foldername,j))
        pix.save("./img/%s/page_%s.png" % (foldername,j))
    return output_ls

def checkFolder(pdf_path):
    if os.path.isdir(pdf_path):
        file_list = os.listdir(pdf_path)
        checkPDF(pdf_path,file_list)
        return True
    return False

def checkPDF(input_path, file_list):
    if not file_list:
        print("\nNo files found")
        return None
    else:
        for file in file_list:
            pdf_path = input_path+"/"+file
            if checkFolder(pdf_path):
                continue
            print("Processing: ",pdf_path)
            pdf2imgs(pdf_path)

def main(input_path):
    checkFolder(input_path)
    print("Done All!!")

if __name__ == "__main__":
    input_path = "./dataset"
    main(input_path)