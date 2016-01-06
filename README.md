# Network_SNPs
A framework for network analysis and display of SNPs

The group consisted of 6 members.

Presentation of the work is available here: https://docs.google.com/presentation/d/1PzQrERWxcQQvih6TLuF4IBvmNCFe7D253Qm5UWPAWfA/edit?usp=sharing

#Introduction
Our work focuses on using network analysis methods to aid analysis of variant calls. Centrality measure is used as.

# Input
<p><strong>1</strong>
</p>
<p><strong>2</strong>
</p>
# Output
<strong>Filenames:</strong>
<p><i>output:</i>  3-column file with gene names, degrees and betweenness of genes.
   <p>
        <pre>
                <code>
                # From this output, it would be smart to focus on CD3EAP since it
                # has the highest centrality and degree measurement
                # Example:
                gene	degrees	btw_centrality
                CD3EAP	500	0.377719224858
                TMC1	30	0.000297257109932
                LRP8	30	0.000768086055561
                SLC30A6	26	0.000223232830101
                ZNF234	22	0.000146138740468
                MYBBP1A	20	0.000310454619974
                HHIPL2	41	0.000495219919278
                CYP2B6	41	0.000465664109724
                CLDN20	17	5.61032381821e-05
                </code>
        </pre>
   </p>
</p>
<p><i>pngs/</i>: This folder has a figure for each input gene and its neighbor genes.
</p>
<p><i>xml_format/</i>: This folder has the xml format of the subnetworks in the pngs folder.
</p>
<p><i>xml_format</i>: This folder has the xml format of the subnetworks in the pngs folder.
</p>
#Running the pipeline
<code>
testing
</code>

