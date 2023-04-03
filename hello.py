import streamlit as st
import os
from openbabel import pybel
import zipfile
import py3Dmol
import pandas as pd



# Sidebar
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt'])
mol_list_f =[]
if st.button("Convert and download"):
    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False)
    st.header('**Original input data**')
    st.write(load_data)
    mol_list = list(load_data.iloc[:,0])
    output_files = []
    output_format = 'mol2'
    #out=pybel.Outputfile(filename='mol.mol2',format='mol2',overwrite=True)
    for index,smi in enumerate(mol_list):
        mol=pybel.readstring(string=smi,format='smiles')
        mol.title='mol_'+str(index)
        mol.make3D('mmff94s')
        mol.localopt(forcefield='mmff94s', steps=500)
        output_file = 'mol_'+str(index)+'.mol2'
        mol.write(format=output_format, filename=output_file, overwrite=True)
        output_files.append(output_file)

           
    #Combine output files into single ZIP file
    output_zip = "converted_molecule.zip"
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for output_file in output_files:
            zipf.write(output_file)

    with open(output_zip, "rb") as f:
        st.download_button(
            label=f"Download converted molecules in nol2 format",
            data=f.read(),
            file_name=output_zip,
            mime="application/zip",
        )
        
        # Delete input and output files
        os.remove(output_zip)
else:
    st.warning("Please upload a valid file containing SMILES strings.")