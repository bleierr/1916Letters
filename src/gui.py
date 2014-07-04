'''
Created on 14 May 2014

@author: Bleier
'''
from Tkinter import *
import tkFileDialog
from txt_classes import TxtCorpus, TxtItem
import importer, analyse, outputter
from lxml import etree
import os

  

class Application(Frame):
    
    def __init__(self, master=None):
        """
        Establish the window structure, leaving some widgets accessible
        as app instance variables. Connect button clicks to the 'search' methods
        and subject double-clicks to display_letters method.
        """
        Frame.__init__(self, master)
        for i in range(8):
            self.master.rowconfigure(i, weight=1)
            self.master.columnconfigure(i, weight=1)
        
        self.infobox = Text(self.master)
        self.infobox.grid(row=0, column=0, columnspan=3, sticky=W+N+S+E)
        self.inputframe = Frame(self.master, borderwidth=5, width=300)
        self.inputframe.grid(row=1, column=0, columnspan=3, sticky=W+N+S+E)
        
        for i in range(8):
            self.inputframe.rowconfigure(i, weight=1)
            self.inputframe.columnconfigure(i, weight=1)
        
        self.currentdir = os.path.dirname(os.getcwd())
        
        # make the search dir buttons
        # defining options for opening a directory
        self.dir_opt = doptions = {}
        doptions['initialdir'] = self.currentdir
        doptions['mustexist'] = False
        doptions['parent'] = root
        
        #source files directory
        self.sourcedir = Entry(self.inputframe, width=50)
        self.sourcedir.grid(row=0, column=0, columnspan=5, sticky=W+N+S+E)
        
        doptions["title"] = "find a source file(s) directory"
        b1 = Button(self.inputframe, text='source file(s) directory', command=lambda: self.askxdisplay_dir(self.sourcedir, doptions))
        b1.grid(row=0, column=6, columnspan=2)
        
        
        #default file options
        self.file_opt = foptions = {}
        foptions['defaultextension'] = '.txt'
        foptions['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        foptions['initialdir'] = self.currentdir
        foptions['initialfile'] = 'myfile.txt'
        foptions['parent'] = root
        
        # use excel file as source file
        self.excelFile = Entry(self.inputframe, width=50)
        self.excelFile.grid(row=1, column=0, columnspan=5, sticky=W+N+S+E)
        
        foptions['title'] = 'find an excel file'
        b_excel = Button(self.inputframe, text='search excel file', command=lambda: self.askxdisplay_file(self.excelFile, foptions))
        b_excel.grid(row=1, column=6, columnspan=2)
        
        
        # use existing corpus
        self.existCorpus = Entry(self.inputframe, width=50)
        self.existCorpus.grid(row=2, column=0, columnspan=5, sticky=W+N+S+E)
        
        foptions['title'] = 'find an existing corpus'
        b2 = Button(self.inputframe, text='search for existing corpus', command=lambda: self.askxdisplay_file(self.existCorpus, foptions))
        b2.grid(row=2, column=6, columnspan=2)
        
        # add similarity comparison text
        self.simfile = Entry(self.inputframe, width=50)
        self.simfile.grid(row=3, column=0, columnspan=5, sticky=W+N+S+E)
        
        foptions['title'] = 'find text to compare to corpus'
        b3 = Button(self.inputframe, text='search text to compare', command=lambda: self.askxdisplay_file(self.simfile, foptions))
        b3.grid(row=3, column=6, columnspan=2)
        
        """
        # stopword list directory
        self.stoplistfile = Entry(self.inputframe, width=50)
        self.stoplistfile.grid(row=3, column=0, columnspan=5, sticky=W+N+S+E)

        foptions['title'] = 'find a stopword file'
        b4 = Button(self.inputframe, text='search stopword file', command=lambda: self.askxdisplay_file(self.stoplistfile, foptions))
        b4.grid(row=3, column=6, columnspan=2)
        """
        b5 = Button(self, text='generate stats', command=self.runanalysis)
        b5.grid(row=4, column=6, columnspan=2)
        
        
        
        self.search_transc_lst = []
        self.search_title_lst = []
        
        self.grid(sticky=W+E+N+S)
        l0 = Label(self, text="Generate Models", font=("Helvetica", 16))
        l0.grid(row=4, column=1, columnspan=2)
        
        
    def runanalysis(self):
        """
        get files
        """
        sourcedir = self.sourcedir.get()
        existCorpus = self.existCorpus.get()
        simfile = self.simfile.get()
        excelFile = self.excelFile.get()
        
        if sourcedir and existCorpus:
            self.infobox.insert(INSERT, "Too many fields filled out! Not sure where to get the data from!")
            return None
        if sourcedir and excelFile:
            self.infobox.insert(INSERT, "Too many fields filled out! Not sure where to get the data from!")
            return None
        if existCorpus and excelFile:
            self.infobox.insert(INSERT, "Too many fields filled out! Not sure where to get the data from!")
            return None
        
        
        if simfile:
            if os.path.exists(simfile):
                try:
                    f = open(simfile, "r")
                    test_doc = f.read().lower().split()
                    f.close()
                except:
                    self.infobox.insert(INSERT, "There is an error with the file that was imported for similarity testing. It seems to be no .txt file!")
                    return None
            else:
                self.infobox.insert(INSERT, "The file path to the file for similarity testing is not correct!")
                return None
        
        #ensures that the chosen corpus file is the right type and contains the correct data
        if existCorpus:
            if os.path.exists(existCorpus):
                try:
                    for item in corpus.get_txtitems():
                        if not isinstance(item, TxtItem):
                            self.infobox.insert(INSERT, "The chosen corpus seems to contain no TxtItmes!")
                            return None
                        corpus = TxtCorpus(existCorpus)
                        vect_corpus = corpus.get_vector_corpus()
                        dictionary = corpus.get_dict()
                except MemoryError:
                    self.infobox.insert(INSERT, "The chosen corpus seems to be no TxtCorpus binary file!")
                    return None
            else:
                self.infobox.insert(INSERT, "The file path to the existing text corpus is not correct!")
                return None
        elif excelFile:
            head, tail = os.path.split(excelFile)
            corpus = importer.get_texts_from_Excel(excelFile, head)
            vect_corpus = corpus.get_vector_corpus()
            print len(vect_corpus)
            dictionary = corpus.get_dict()
            print len(dictionary)    
        else:
            try:
                corpus = importer.get_texts_from_files(sourcedir, sourcedir)
                vect_corpus = corpus.get_vector_corpus()
                print "Txt"
                dictionary = corpus.get_dict()
            except WindowsError:
                self.sourcedir.delete(0, END)
                self.sourcedir.insert(END, "Please select a valid source dir containing valid text files!")
                return None
        toPrint = {}
        files = []
        for item in corpus.get_txtitems():
            files.append(item.get_id())
        toPrint["filenames"] = files
        topics = analyse.make_topics(vect_corpus, dictionary, 20)
        toPrint["topics"] = topics
        doc2topic = analyse.topics2docs(vect_corpus, dictionary, 20)
        toPrint["topic_sim"] = [item for item in doc2topic]
        
        if simfile:
            #prepare the sample text for similarity testing
            sims = analyse.doc_similarity(vect_corpus, dictionary, test_doc, 20)
            toPrint["doc_sim"] = (str(test_doc), [item for item in zip(sims, range(corpus.number_of_txts()))])
        
        s = outputter.data_to_output_string(toPrint)
        f = open("letters_stat.txt", "w")
        f.write(s)
        f.close()
        
        t_lda = analyse.make_lda_topics(vect_corpus, dictionary, num_topics=15, passes=10)
        
        f = open("lda_topics_gensim.txt", "w")
        for t in t_lda:
            f.writelines(t)
        f.close()
        
        #print text to files
        """
        os.mkdir("corpusfiles")
        for name, tokens in corpus.get_tokens():
            f = open("corpusfiles" + os.sep + str(name) + ".txt", "w")
            for t in tokens:
                f.write(t+" ")
            f.close()
        """ 
        print "done!"
        
            
    def display_TxtItem(self, event):
        """
        Display the txt item corresponding to the title in the List box that the user just
        clicked on.
        """
        indexes = self.msgsubs.curselection()
        if len(indexes) != 1:
            return
        #clears the message box
        self.letterDisp.delete(1.0, END)
        if len(self.search_transc_lst) > 0:
            l = self.search_transc_lst[int(indexes[0])]
        elif len(self.search_title_lst) > 0:
            l = self.search_title_lst[int(indexes[0])]
        else:
            l = self.letters[int(indexes[0])]
        for key, val in l.__dict__.items():
            self.letterDisp.insert(INSERT, "\n{0}:\n {1}\n".format(key, val))
            if isinstance(val, etree._Element):
                self.letterDisp.insert(INSERT, "Content lxml etree._Element:\n {0}\n{1}\n".format(etree.tostring(val), "-"*50))
            #self.letterDisp.insert(INSERT, )
        self.letterDisp.insert(END, "\n")
        
    def askxdisplay_dir(self, inputField, options):
        """
        Allows search for a file directory in dialoge box, and display in input field.
        Parameter inputField is the input field where the file path will be displayed.
        Parameter options is a dictionary of options, valid arguments to be passed on the askdirectory()
        """
        inputField.delete(0, END)
        dirname = tkFileDialog.askdirectory(**options)
        inputField.insert(END, dirname)
        
    def askxdisplay_file(self, inputField, options):
        """
        Allows search for a file in dialoge box, and display in input field.
        Parameter inputField is the input field where the file path will be displayed.
        Parameter options is a dictionary of options, valid arguments to be passed on the askopenfilename()
        """
        inputField.delete(0, END)
        filename = tkFileDialog.askopenfilename(**options)
        inputField.insert(END, filename)

   
        
if __name__ == "__main__":
    root= Tk()
    app = Application(master=root)
    #app.search_mail()
    app.mainloop()
        