# Uses networkx library to calculate the degrees,betweenness centrality 
# of the input genes. Also creates the XML format and PNG figure 
# of the subnetwork with the input gene.
#
#
# Command line: python networkx_snps.py --input <file> --network <network> --out
#
# pip install networkx
#
# Input: 1. 1-column input file with gene names (input)
#        2. 2-column input file with genes in column 1 and 2 that
#           are interacting (network)
#        3. Directory name for ouput (out)
#
# Output: 1. Figures of subnetworks --> <out directory>/pngs/
#         2. XML format of subnetworks --> <out directory>/xm_format/
#         3. <out directory>/output

import argparse
import networkx
import matplotlib
matplotlib.use('Agg')
import os

def write_networks(network,filename,outdir):
    if not os.path.exists("%s/pngs" % outdir):
        os.makedirs("%s/pngs" % outdir)
    outpng = "%s/pngs/%s.png" % (outdir,filename)
    networkx.draw_networkx(network,with_labels=True)
    matplotlib.pyplot.axis("off")
    matplotlib.pyplot.savefig(outpng)
    matplotlib.pyplot.close()
    if not os.path.exists("%s/xml_format" % outdir):
        os.makedirs("%s/xml_format" % outdir)
    outxmlfn = "%s/xml_format/%s.xml" % (outdir,filename)
    networkx.write_graphml(network,outxmlfn)

# Run all the analysis here
def network_analysis(gene_list,network_file,outdir):
    outfn = "%s/output" % outdir
    f = open(outfn,'w')
    f.write("gene\tdegrees\tbtw_centrality\n")
    network = networkx.read_adjlist(network_file)
    print "Number of edges in input graph: %s" % network.number_of_edges()
    print "Number of nodes in input graph: %s" % network.number_of_nodes()
    subnetwork = network.subgraph(gene_list)
    print "Number of edges in subgraph: %s" % subnetwork.number_of_edges()
    print "Number of nodes in subgraph: %s" % subnetwork.number_of_nodes()
    bwt_central = networkx.betweenness_centrality(subnetwork)
    degrees = subnetwork.degree(gene_list)
    for gene in gene_list:
        # Number of degrees
        if gene in degrees:
            num_degrees = degrees[gene]
        else:
            num_degress = "NA"
        # Betweenness centrality
        if gene in bwt_central:
            btw_gene = bwt_central[gene]
        else:
            btw_gene = "NA"
        # File with neighbor nodes
        if subnetwork.has_node(gene):
            neighbors = list(networkx.all_neighbors(subnetwork,gene))
            edges = [(unicode(gene),neighbor) for neighbor in neighbors]
            neighbor_networks = networkx.from_edgelist(edges)
            write_networks(neighbor_networks,gene,outdir)
        f.write("%s\t%s\t%s\n" % (gene,num_degrees,btw_gene))
    f.close()

# Get a list of gene names
def load_gene_list(input_file):
    genes = []
    with open(input_file,'r') as f:
        for line in f:
            genes.append(line.rstrip())
    return genes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--network', type=str,required=True)
    parser.add_argument('--out', type=str,required=True)
    args = parser.parse_args()
    gene_list = load_gene_list(args.input)
    network_analysis(gene_list,args.network,args.out)

