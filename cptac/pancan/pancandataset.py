#   Copyright 2018 Samuel Payne sam_payne@byu.edu
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import cptac
import cptac.exceptions as ex
import pandas as pd
import logging
import cptac.utils as ut

class PancanDataset:

    def __init__(self, cancer_type, version, no_internet):
        """Initialize variables for a PancanDataset object."""

        self._cancer_type = cancer_type
        self._version = version
        self._datasets = {} # Child class __init__ needs to fill this
        self._joining_dataset = None
        
        #ignore logging messages
        logger = logging.getLogger()
        logger.setLevel(logging.CRITICAL)
        

    # Clinical table getters
    def get_clinical(self, source = 'mssm', tissue_type="both", imputed=False):
        """Get the clinical dataframe from the specified data source."""
        return self._get_dataframe("clinical", source, tissue_type, imputed=imputed)
    
    def get_demographic(self, source = 'mssm', tissue_type="both", imputed=False):
        """Get the demographic dataframe from the specified data source."""
        return self._get_dataframe("demographic", source, tissue_type, imputed=imputed)
    
    def get_medical_conditions(self, source = 'mssm', tissue_type="both", imputed=False):
        """Get the medical_conditions dataframe from the specified data source."""
        return self._get_dataframe("medical_conditions", source, tissue_type, imputed=imputed)
    
    def get_previous_cancer(self, source = 'mssm', tissue_type="both", imputed=False):
        """Get the previous_cancer dataframe from the specified data source."""
        return self._get_dataframe("previous_cancer", source, tissue_type, imputed=imputed)
    
    def get_cancer_diagnosis(self, source = 'mssm', tissue_type="both", imputed=False):
        """Get the cancer_diagnosis dataframe from the specified data source."""
        return self._get_dataframe("cancer_diagnosis", source, tissue_type, imputed=imputed)
    
    def get_followup(self, source = 'mssm', tissue_type="both", imputed=False):
        """Get the followup dataframe from the specified data source."""
        return self._get_dataframe("followup", source, tissue_type, imputed=imputed)

    # Quantitative table getters
    def get_acetylproteomics(self, source, tissue_type="both", imputed=False):
        """Get the acetylproteomics dataframe from the specified data source."""
        return self._get_dataframe("acetylproteomics", source, tissue_type, imputed=imputed)

    def get_circular_RNA(self,source = "bcm", tissue_type="both", imputed=False):
        """Get a circular RNA dataframe from the specified data source."""
        return self._get_dataframe("circular_RNA", source, tissue_type, imputed=imputed)
    
    def get_CNV(self,source = "washu", tissue_type="both", imputed=False):
        """Get a CNV dataframe from the specified data source."""
        return self._get_dataframe("CNV", source, tissue_type, imputed=imputed)

    def get_deconvolution(self, deconv_algorithm=None, source='washu', tissue_type="both", imputed=False):
        """Get a deconvolution dataframe from the specified data source.
        
        Parameters:
        deconv_algorithm (str):  Choose an alorithm. Acceptable values are ['cibersort', 'xcell']. 
        source (str): Select data generated by a certain institution. Available sources are ['washu']. Defaults to 'washu'. 
        """
        valid_algs = ['cibersort', 'xcell']
        if deconv_algorithm is None or deconv_algorithm not in valid_algs:
            raise ex.InvalidParameterError(f"Please pass a valid value to the 'deconv_algorithm' parameter to specify which algorithm you want deconvolution data from. Valid options are {valid_algs}.")

        return self._get_dataframe(deconv_algorithm, source, tissue_type, imputed=imputed)
    
    def get_miRNA(self, source = 'washu', miRNA_type = 'total', tissue_type="both", imputed=False):
        """Get miRNA dataframe from the specified data source.
        
        Parameters:
        source (str): Select data generated by a certain institution. Available sources are ['washu']. Defaults to 'washu'.
        miRNA_type (str): Choose the type of miRNA molecules measured. Acceptable values are ['total', 'precursor', 'mature'].
        """
        return self._get_dataframe(miRNA_type+'_miRNA', source, tissue_type, imputed=imputed)
    
    def get_phosphoproteomics(self, source = "umich", tissue_type="both", imputed=False):
        """Get the phosphoproteomics dataframe from the specified data source."""
        return self._get_dataframe("phosphoproteomics", source, tissue_type, imputed=imputed)

    def get_proteomics(self, source = "umich", tissue_type="both", imputed=False):
        """Get the proteomics dataframe from the specified data source."""
        return self._get_dataframe("proteomics", source, tissue_type, imputed=imputed)

    def get_somatic_mutation(self, source = "harmonized", tissue_type="both", imputed=False):
        """Get the somatic mutation dataframe from the specified data source."""
        ''' source (str): Select data generated by a certain institution. Default is harmonized. "washu" is also available'''
        return self._get_dataframe("somatic_mutation", source, tissue_type, imputed=imputed)
    
    def get_transcriptomics(self, source, tissue_type="both", imputed=False):
        """Get the transcriptomics dataframe from the specified data source."""
        """source (str): Select data generated by a certain institution. Available sources are ['washu','bcm','broad']."""
        return self._get_dataframe("transcriptomics", source, tissue_type, imputed=imputed)
    
    def get_tumor_purity(self, source = 'washu', tissue_type="both", imputed=False):
        """Get the tumor purity dataframe from the specified data source."""
        return self._get_dataframe("tumor_purity", source, tissue_type, imputed=imputed)

    # Join functions
    def join_omics_to_omics(
        self, 
        df1_name, 
        df2_name,
        df1_source,
        df2_source,
        genes1=None, 
        genes2=None, 
        how="outer", 
        quiet=False, 
        tissue_type="both"
    ):
        
        df1_name = f"{df1_source}_{df1_name}"
        df2_name = f"{df2_source}_{df2_name}"
        
        return self._joining_dataset.join_omics_to_omics(
            df1_name=df1_name, 
            df2_name=df2_name,
            genes1=genes1, 
            genes2=genes2, 
            how=how, 
            quiet=quiet, 
            tissue_type=tissue_type
        )
    
    def join_omics_to_mutations(
        self,
        omics_df_name,
        omics_source,
        mutations_genes,  
        omics_genes=None, 
        mutations_filter=None, 
        show_location=True, 
        how="outer", 
        quiet=False,
        tissue_type="both",
        mutation_cols=["Mutation","Location"]
     
    ):
        omics_df_name = f"{omics_source}_{omics_df_name}"
      
        return self._joining_dataset.join_omics_to_mutations(
            omics_df_name = omics_df_name,
            mutations_genes = mutations_genes,
            omics_genes=omics_genes,
            mutations_filter=mutations_filter,
            show_location=show_location,
            how=how,
            quiet=quiet,
            tissue_type=tissue_type,
            mutation_cols=mutation_cols
        )
         
        
    # Help functions
    def get_cancer_type(self):
        return self._cancer_type
    
    def list_sources_data(self):
        """Print which sources provide each data type.
        
        Parameters:
        print_list (bool, optional): Whether to print the list. Default is True. Otherwise, it's returned as a string.
        """

        # This dict will be keyed by data type, and the values will be each source that provides that data type
        data_sources = {}

        for source in sorted(self._datasets.keys()):
            for df_name in sorted(self._datasets[source]._data.keys()):

                if df_name in ["cibersort", "xcell"]:
                    df_name = f"deconvolution_{df_name}" # For clarity

                if df_name in data_sources.keys():
                    data_sources[df_name][0] += f", {source}"
                else:
                    data_sources[df_name] = [source]

        data_sources = pd.\
        DataFrame(data_sources).\
        transpose().\
        sort_index().\
        reset_index()

        data_sources.columns=["Data type", "Available sources"]

        return data_sources
        


    # "Private" methods
    def _get_dataframe(self, name, source, tissue_type, imputed):
        """Check that a given dataframe from a given source exists, and return a copy if it does."""

        if imputed:
            name = name + "_imputed"

        if source in self._datasets.keys():
            return self._datasets[source]._get_dataframe(name, tissue_type)
        else:
            raise ex.DataSourceNotFoundError(f"Data source {source} not found for the {self._cancer_type} dataset.")

    def _get_version(self, source):
        if self._version == "latest":
            return self._version
        elif type(self._version) is dict:
            return self._version[source]
        else:
            return self._version
        
    def get_genotype_all_vars(self, mutations_genes, omics_source, mutations_filter=None, show_location=True, mutation_hotspot=None):
        """Return a dataframe that has the mutation type and wheather or not it is a multiple mutation
        Parameters:
        mutation_genes (str, or list or array-like of str): The gene(s) to get mutation data for.
        mutations_filter (list, optional):  List of mutations to prioritize when filtering out multiple mutations, in order of priority.
        omics_source(str): Source of omics data ex "bcm", "washu", "broad", "umich"
        show_location (bool, optional): Whether to include the Location column from the mutation dataframe. Defaults to True.
        mutation_hotspot (optional): a list of hotspots
        """

        #If they don't give us a filter, this is the default.
           
        mutations_filter = ["Deletion",
                                    'Frame_Shift_Del', 'Frame_Shift_Ins', 'Nonsense_Mutation', 'Nonstop_Mutation', #tuncation
                                    'Missense_Mutation_hotspot',
    	                           'Missense_Mutation',
                                    'Amplification',
                                    'In_Frame_Del', 'In_Frame_Ins', 'Splice_Site' ,
                                    'De_Novo_Start_Out_Frame' ,'De_Novo_Start_In_Frame', 
                                    'Start_Codon_Ins', 'Start_Codon_SNP', 
                                    'Silent',
                                    'Wildtype']

        truncations = ['Frame_Shift_Del', 'Frame_Shift_Ins', 'Nonsense_Mutation', 'Nonstop_Mutation', 'Splice_Site']
        missenses = ['In_Frame_Del', 'In_Frame_Ins', 'Missense_Mutation']
        noncodings = ["Intron", "RNA", "3'Flank", "Splice_Region", "5'UTR", "5'Flank", "3'UTR"]



        #check that gene is in the somatic_mutation DataFrame
        somatic_mutation = self.get_somatic_mutation()
        if mutations_genes not in somatic_mutation["Gene"].unique(): #if the gene isn't in the somacic mutations df it will still have CNV data that we want
            def add_del_and_amp_no_somatic(row):
                if row[mutations_genes] <= -.2:
                    mutations = 'Deletion'

                elif row[mutations_genes] >= .2:
                    mutations = 'Amplification'
                else:
                    mutations = "No_Mutation"

                return mutations
            
            cnv = self.get_CNV(source = omics_source)
            #drop the database index from ccrcc and brca
            if isinstance(cnv.keys(), pd.core.indexes.multi.MultiIndex):
                drop = ['Database_ID']
                cnv = ut.reduce_multiindex(df=cnv, levels_to_drop=drop)       
            gene_cnv = cnv[[mutations_genes]]
            mutation_col = gene_cnv.apply(add_del_and_amp_no_somatic, axis=1)
            df = gene_cnv.assign(Mutation = mutation_col)
            return df


        #combine the cnv and mutations dataframe
        combined = self.join_omics_to_mutations(omics_df_name="CNV", mutations_genes=mutations_genes, omics_genes=mutations_genes, omics_source = omics_source)
                

        #drop the database index 
        drop = ['Database_ID']
        combined = ut.reduce_multiindex(df=combined, levels_to_drop=drop)


        #If there are hotspot mutations, append 'hotspot' to the mutation type so that it's prioritized correctly
        def mark_hotspot_locations(row):
            #iterate through each location in the current row
            mutations = []
            for location in row[mutations_genes+'_Location']:
                if location in mutation_hotspot: #if it's a hotspot mutation
                    #get the position of the location
                    position = row[mutations_genes+'_Location'].index(location)
                    #use that to change the correct mutation
                    mutations.append(row[mutations_genes+"_Mutation"][position] + "_hotspot")
                else:
                    # get the position of the location
                    position = row[mutations_genes+'_Location'].index(location)
                    mutations.append(row[mutations_genes+"_Mutation"][position])
            return mutations

        if mutation_hotspot is not None:
            combined['hotspot'] = combined.apply(mark_hotspot_locations, axis=1)
            combined[mutations_genes+"_Mutation"] = combined['hotspot']
            combined = combined.drop(columns='hotspot')
     

        # Based on cnv make a new column with mutation type that includes deletions and amplifications
        def add_del_and_amp(row):
            if row[mutations_genes+ "_" + omics_source + "_CNV"] <= -.2:
                mutations = row[mutations_genes+"_Mutation"] + ['Deletion']
                locations = row[mutations_genes+'_Location']+['Deletion']

            elif row[mutations_genes + "_" + omics_source+"_CNV"] >= .2:
                mutations = row[mutations_genes+"_Mutation"] + ['Amplification']
                locations = row[mutations_genes+'_Location']+['Amplification']
            else:
                mutations = row[mutations_genes+"_Mutation"]
                locations = row[mutations_genes+"_Location"]

            return mutations, locations


        combined['mutations'], combined['locations'] = zip(*combined.apply(add_del_and_amp, axis=1))
       
        #now that we have the deletion and amplifications, we need to prioritize the correct mutations.
        def sort(row):
            sortedcol = []
            location = []
            chosen_indices = []
            sample_mutations_list = row['mutations']
            sample_locations_list = row['locations']
            if len(sample_mutations_list) == 1: #if there's only one mutation in the list
                sortedcol.append(sample_mutations_list[0])
                location.append(sample_locations_list[0])

            else:
                for filter_val in mutations_filter: # This will start at the beginning of the filter list, thus filters earlier in the list are prioritized, like we want
                    if filter_val in sample_mutations_list:
                        chosen_indices = [index for index, value in enumerate(sample_mutations_list) if value == filter_val]
                    if len(chosen_indices) > 0: # We found at least one mutation from the filter to prioritize, so we don't need to worry about later values in the filter priority list
                        break

                if len(chosen_indices) == 0: # None of the mutations for the sample were in the filter, so we're going to have to use our default hierarchy
                    for mutation in sample_mutations_list:
                        if mutation in truncations:
                            chosen_indices += [index for index, value in enumerate(sample_mutations_list) if value == mutation]

                if len(chosen_indices) == 0: # None of them were in the filter, nor were truncations, so we'll grab all the missenses
                    for mutation in sample_mutations_list:
                        if mutation in missenses:
                            chosen_indices += [index for index, value in enumerate(sample_mutations_list) if value == mutation]

                if len(chosen_indices) == 0: # None of them were in the filter, nor were truncations, nor missenses, so we'll grab all the noncodings
                    for mutation in sample_mutations_list:
                        if mutation in noncodings:
                            chosen_indices += [index for index, value in enumerate(sample_mutations_list) if value == mutation]

                soonest_mutation = sample_mutations_list[chosen_indices[0]]
                soonest_location = sample_locations_list[chosen_indices[0]]
                chosen_indices.clear()
                sortedcol.append(soonest_mutation)
                location.append(soonest_location)

            return pd.Series([sortedcol, location],index=['mutations', 'locations'])

        df = combined.apply(sort, axis=1)
        combined['Mutation'] = df['mutations']
        combined['Location'] = df['locations']

        #get a sample_status column that says if the gene has multiple mutations (including dletion and amplification)
        def sample_status(row):
            if len(row['mutations']) > 1: #if there's more than one mutation
                if len(row['mutations']) == 2 and "Wildtype_Tumor" in row['mutations']: #one of the mutations might be a "wildtype tumor"
                    status ="Single_mutation"

                elif len(row['mutations']) == 2 and "Wildtype_Normal" in row['mutations']:
                    status ="Single_mutation"

                else:
                    status = "Multiple_mutation"
            else:
                if row["mutations"] == ["Wildtype_Normal"]:
                    status = "Wildtype_Normal"
                elif row['mutations'] == ['Wildtype_Tumor']:
                    status = "Wildtype_Tumor"
                else:
                    status = "Single_mutation"

            return status
        combined['Mutation_Status'] = combined.apply(sample_status, axis=1)

        #drop all the unnecessary Columns
        df = combined.drop(columns=[mutations_genes+ "_" + omics_source +"_CNV", mutations_genes+"_Mutation", mutations_genes+"_Location", mutations_genes+"_Mutation_Status", 'Sample_Status', 'mutations','locations'])
        df['Mutation'] = [','.join(map(str, l)) for l in df['Mutation']]
        df['Location'] = [','.join(map(str, l)) for l in df['Location']]
        if show_location == False: df = df.drop(columns="Location") #if they don't want us to show the location, drop it
       
        return df