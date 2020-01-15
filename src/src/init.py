import utils 
import argparse
import logging
import sys
import pickle
import os
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser(description='Calculating the IDT metric')
parser.add_argument('--dataset' , help = 'path of the meta data file dataset')
parser.add_argument('--dumps' , help = 'path to store the pickled files') 
parser.add_argument('--graph_path', help = 'path to citation-cited csv')

args = parser.parse_args()
logging.StreamHandler(sys.stdout)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' , level=logging.INFO) 

if __name__ == '__main__':
    
    paper_year_dict = {}
    logging.info('Parsing Year from dataset')
    
    for file in os.listdir(args.dataset):
        if file.startswith(('P','RM')):
            paper_year_dict = utils.parse_year(args.dataset+file, paper_year_dict)

    logging.info('Serialising Paper- Year Dictionary') 
    utils.dump_file(args.dumps , 'paper_year_dict' , paper_year_dict)
    
    global_citation_graph = ''
    logging.info('Parsing Dataset')
   
    global_citation_graph = utils.create_graph(args.graph_path, paper_year_dict )
    logging.info('Serialising Global Citation Graph')
    utils.dump_file(args.dumps, 'global_citation_graph_full' , global_citation_graph)

   
    logging.info('Removing Cycles')
    global_citation_graph = utils.remove_cycles(global_citation_graph) 
    logging.info('Removed Cycles')
    logging.info('Serialising Decyclised Graph')
    utils.dump_file(args.dumps , 'global_citation_graph_full_decyclised' , global_citation_graph)
    logging.info('Creating  IDTs ...')
    
    #global_citation_graph = utils.get_pickle_dump("../dumps", "G_without_cycles")

    IDT_Dict = utils.IDT_init(global_citation_graph)
    utils.dump_file(args.dumps , 'IDT_Dict' , IDT_Dict)
    logging.info('Serialising IDT Dictionary')
    global_depth_breath = utils.global_depth_breadth(IDT_Dict)
    utils.dump_file(args.dumps , 'global_depth_breath_citation_dict' , global_depth_breath)
    logging.info('Serialising global depth bredth citation Dictionary')
    NID_dict, IDI_dict = utils.get_NID_IDI(IDT_Dict) 
    utils.dump_file(args.dumps , 'NID_dict' , NID_dict)
    utils.dump_file(args.dumps , 'IDI_dict' , IDI_dict)
    logging.info('Serialising NID and IDI Dictionary')
