#
# run.py file.
# Command line: python networkx_snps.py --input <file> --network <network>
#
# pip install networkx
# Networks should have gene names (concensus among networks (?))
# Example:
# python network_snps.py --input test/gene_list --network test/graph --out test/

import argparse
import networkx
import itertools
import matplotlib
matplotlib.use('Agg')
import HTML
import os

def html_report(gene_list,analysis,outdir):
    outfn = "%s/report.html" % outdir
    table_data = []
    for counter, gene in enumerate(gene_list):
        row = []
        row.append(gene)
        for measure in analysis:
            row.append(analysis[measure][counter])
        table_data.append(row)
    header = ["gene"]
    for measure in analysis:
        header.append(measure)
    htmlcode = HTML.table(table_data,header_row=header)
    with open(outfn,'w') as f:
        f.write(htmlcode)

# Get cliques
def get_cliques(network,gene,outdir):
    if not os.path.exists("%s/clique" % outdir):
        os.makedirs("%s/clique" % outdir)
    cliques = networkx.cliques_containing_node(network,nodes=gene)
    output_cliques = []
    for counter,clique in enumerate(cliques):
        if len(clique) > 2:
            out_clique = list(itertools.combinations(clique,2))
            out_clique = networkx.from_edgelist(out_clique)
            out_cliquepng = "%s/clique/%s.%s.png" % (outdir,gene,counter)
            networkx.draw_networkx(out_clique,with_labels=True)
            matplotlib.pyplot.axis("off")
            matplotlib.pyplot.savefig(out_cliquepng)
            matplotlib.pyplot.close()
            out_cliquefn = "%s/clique/%s.%s.xml" % (outdir,gene,counter)
            networkx.write_graphml(out_clique,out_cliquefn)
            output_cliques.append("<a href=\"%s\">clique</a>,<a href=\"%s\">xml format</a>" % (out_cliquepng,out_cliquefn))
    return output_cliques

# return subnetwork
def get_subnetwork(network,gene):
    neighbors = list(networkx.all_neighbors(network,gene))
    edges = [(unicode(gene),neighbor) for neighbor in neighbors]
    for neighbor in neighbors:
        neighbor_neighbors = list(networkx.all_neighbors(network,neighbor))
        add_edges = [(unicode(neighbor),neighbor_neighbor) for neighbor_neighbor in neighbor_neighbors]
        edges += add_edges
    subnetwork = networkx.from_edgelist(edges)
    return subnetwork

# Run all the analysis here
def network_analysis(gene_list,network_file,outdir):
    analysis = {}
    network = networkx.read_adjlist(network_file)
    analysis['SUBGRAPH'] = []
    analysis['BETWEENNESS_CENTRALITY'] = []
    for gene in gene_list:
        subnetwork = get_subnetwork(network,gene)
        bwt_central = networkx.betweenness_centrality(subnetwork)
        cliques = get_cliques(subnetwork,gene,outdir)
        analysis['SUBGRAPH'].append(cliques)
        analysis['BETWEENNESS_CENTRALITY'].append(str(bwt_central[gene]))
    return analysis

# Get a list of gene names
def load_gene_list(input_file):
    genes = []
    with open(input_file,'r') as f:
        for line in f:
            if line.startswith('chr'):
                pass
            else:
                genes.append(line.rstrip())
    return genes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--network', type=str,required=True)
    parser.add_argument('--out', type=str,required=True)
    args = parser.parse_args()
    gene_list = load_gene_list(args.input)
    analysis = network_analysis(gene_list,args.network,args.out)
    html_report(gene_list,analysis,args.out)

