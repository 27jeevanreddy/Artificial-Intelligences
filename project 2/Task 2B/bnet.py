import sys
import copy

def get_prob(temp_argument):
    if temp_argument[0] == "n":
        return (1 - get_prob(temp_argument[1:]))
    given_prob = {"B": 0.001,
                         "E": 0.002,
                         "A|B,E": 0.95,
                         "A|B,nE": 0.94,
                         "A|nB,E": 0.29,
                         "A|nB,nE": 0.001,
                         "J|A": 0.90,"J|nA": 0.05,
                         "M|A": 0.70,"M|nA": 0.01}
    if temp_argument in given_prob:
        return given_prob[temp_argument]

def compute_prob_distribution(list_data):
    super_nodes_in_given_data = {'A': ['B','E'], 
                   'B': None, 
                   'E': None, 
                   'J': ['A'], 
                   'M': ['A']}
    len_list_data = len(list_data)
    if len_list_data == 5:
        final_data_list = []
        for temp_node_value in list_data:
            temp_variable = temp_node_value + "|"
            if temp_node_value[0] == "n":
                parent_node_val = super_nodes_in_given_data[temp_node_value[1:]]
            else:
                parent_node_val = super_nodes_in_given_data[temp_node_value]
            if parent_node_val != None:
                for parent in parent_node_val:
                    if parent in list_data:
                        temp_variable += parent + ","
                    else:
                        temp_variable += "n" + parent + ","
            
            temp_variable = temp_variable[0:len(temp_variable)-1]
            final_data_list.append(temp_variable)
        temp_probablty = 1
        for temp_node_value in final_data_list:
            temp_probablty *= get_prob(temp_node_value)
        return temp_probablty
    else:
        required_variables = ['A', 'B', 'E', 'J', 'M']
        for missing_node in required_variables:
            if missing_node in list_data:
                continue
            else:
                status_node_missing = False
                for array_of_node in list_data:
                    if missing_node == array_of_node[1:]:
                        status_node_missing = True
                        break

                if status_node_missing == True:
                    continue
                else:
                    node_missed = missing_node
                    break
        new_lists_data_plain = copy.deepcopy(list_data)
        last_neg_lists_data = copy.deepcopy(list_data)
        new_lists_data_plain.append(node_missed)
        last_neg_lists_data.append("n"+node_missed)
        return compute_prob_distribution(new_lists_data_plain) + compute_prob_distribution(last_neg_lists_data)

def __main__(argv):
    if "given" in argv:
        address_of_index = argv.index("given")
        successors_of_index = argv[address_of_index+1:]
        numerator_of_given = argv[1:address_of_index] + successors_of_index
        list_data = numerator_of_given
        final_data_list = []
        for temp_node_value in list_data:
            if temp_node_value[1] == "t":
                final_data_list.append(temp_node_value[0])
            else:
                final_data_list.append("n"+temp_node_value[0])
        notations_numerator = compute_prob_distribution(final_data_list)
        list_data = successors_of_index
        final_data_list = []
        for temp_node_value in list_data:
            if temp_node_value[1] == "t":
                final_data_list.append(temp_node_value[0])
            else:
                final_data_list.append("n"+temp_node_value[0])
        notations_denominator = compute_prob_distribution(final_data_list)
        print("Probability = " + str(notations_numerator/notations_denominator))
    else:
        list_data = argv[1:]
        final_data_list = []
        for temp_node_value in list_data:
            if temp_node_value[1] == "t":
                final_data_list.append(temp_node_value[0])
            else:
                final_data_list.append("n"+temp_node_value[0])
        print("Probability = " + str(final_data_list))

__main__(sys.argv)