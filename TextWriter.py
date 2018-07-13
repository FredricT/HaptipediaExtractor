import os
import csv

def writeFiles(devices, connections):

    write_connections(connections)
    write_cite_dist(devices, connections)
    write_PDF_tracker(devices)

    for device in devices:
        device = devices[device]
        os.chdir(device.name)

        write_metadata(device)
        write_sections(device)
        write_figures(device)
        write_references(device)
        write_forward_refs(device, devices)

        os.chdir('..')


def write_PDF_tracker(devices):
    with open("PDF_Names_and_Titles.txt", 'w+', encoding='utf8') as file:
        for device in devices:
            file.write('Data from %s is in %s\n' % (devices[device].pdf, devices[device].name))


def write_connections(connections):
    with open("Cross References.txt", 'w+', encoding='utf8') as file:
        for connection in connections:
            file.write ('%s referenced %s (Cited %s times)\n' % (connection.name, connection.cited, connection.times_cited))
            file.write('Shared Authors:\n')
            if connection.shared_authors != []:
                for author in connection.shared_authors:
                    file.write(author + '\n')
            file.write('Shared References:\n')
            if connection.shared_refs != []:
                for ref in connection.shared_refs:
                    file.write(ref.title + '\n')


def write_metadata(device):
    with open("Authors.txt", 'w+', encoding='utf8') as file:
        if device.authors is not []:
            for author in device.authors:
                file.write(author + '\n')
        else:
            file.write("No Authors Extracted")

    with open("Affiliations.txt", 'w+', encoding='utf8') as file:
        if device.affiliates is not []:
            for affiliate in device.affiliates:
                file.write('Laboratory: %s\n' % affiliate.lab)
                file.write('Department: %s\n' % affiliate.dept)
                file.write('Institution: %s\n\n' % affiliate.institute)

    with open("Publisher.txt", 'w+', encoding='utf8') as file:
        if device.publisher != '':
            file.write(device.publisher)
        else:
            file.write("No Publisher Extracted")


def write_sections(device):
    if not os.path.exists('Sections'):
        os.makedirs('Sections')
    os.chdir('Sections')

    write_abstract(device)
    try:
        with open('Sections.txt', 'w+', encoding='utf8') as file:
            for section in device.sections:
                file.write(section + '\n' + '\n')

                for paragraph in device.sections[section]:
                    file.write(paragraph)

                file.write('\n' + '\n')
    except:
        pass
        # TODO: fix error handling

    os.chdir('..')


def write_abstract(device):
    with open('Abstract.txt', 'w+', encoding='utf8') as file:
        file.write(device.sections['Abstract'])


def write_figures(device):
    os.chdir('Figures')
    for figure_number in device.figures:
        figure_caption = device.figures[figure_number]
        try:
            with open(figure_number + '.txt', 'w+', encoding='utf8') as file:
                file.write(figure_caption)
            # TODO: handle this exception
        except:
            pass
    os.chdir('..')


def write_references(device):
    if not os.path.exists('References'):
        os.makedirs('References')
    os.chdir('References')
    for citation in device.backward_ref:
        with open("[" + str(citation.refNumber) + "].txt", 'w+', encoding='utf8') as file:
            file.write('Title: ' + citation.title + '\n')
            file.write('Authors:\n')
            for author in citation.authors:
                file.write(author + '\n')
            publisher = citation.publisher
            if publisher.name is not None:
                file.write('Publisher: ' + publisher.name + '\n')
            file.write('Date: ' + publisher.date + '\n')
            file.write('Page: ' + publisher.page + '\n')
            file.write('Volume: ' + publisher.volume + '\n')
            file.write('Issue: ' + publisher.date + '\n')
            file.write('Times Cited: ' + str(citation.timesCited) + '\n')

    os.chdir('..')


def write_cite_dist(devices, connections):
    dist = {}
    # for connection in connections:
    #     key = connection.times_cited
    #     if key in dist:
    #         dist[key] = dist[key] + 1
    #     else:
    #         dist[key] = 1
    for device in devices:
        for citation in devices[device].backward_ref:
            key = citation.timesCited
            if key == 5 or key == 6:
                print(device + ' cited ' + citation.title)
            if key in dist:
                dist[key] = dist[key] + 1
            else:
                dist[key] = 1

    with open('Distribution.csv', 'w+', newline='') as file:
        fieldnames = ['times_cited', 'occurance']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted(dist):
            writer.writerow({'times_cited': key, 'occurance': dist[key]})


def write_forward_refs(device, devices):
    with open("Papers That Cited This Paper.txt", 'w+', encoding='utf8') as file:
        for ref in device.forward_ref:
            forward_ref = devices[ref]
            file.write(forward_ref.title + "AND CITED " + str(forward_ref.timesCited) + " TIMES" + '\n')













