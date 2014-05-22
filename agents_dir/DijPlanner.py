# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from . logEnvironmentModule import *
from . errorObjs import *

__all__ = ["DijPlanner"]


class DijPlanner(LogAgent):

    """First planner."""

    def __init__(self):
        super(DijPlanner, self).__init__()

    @staticmethod
    def where_is(status, item, airport_only=False):
        print("WHERE IS", item)
        if item in status.airports:
            return item
        for airport_name, airport_obj in status.airports.items():
            if item in airport_obj:
                return airport_name
            for airplane_name, airplane_obj in airport_obj.airplanes.items():
                if item in airplane_obj:
                    return airplane_name if not airport_only else airport_name

    @staticmethod
    def get_target_place(goal, target):
        for place, objs in goal.items():
            if target in objs:
                return place

    # 1  function Dijkstra(Grafo, sorgente):
    # 2      For each vertice v in Grafo:                               // Inizializzazione
    # 3          dist[v] := infinito ;                                  // Distanza iniziale sconosciuta
    # 4                                                                 // dalla sorgente a v
    # 5          precedente[v] := nondefinita ;                             // Nodo precedente in un percorso ottimale
    # 6      end for                                                    // dalla sorgente
    # 7
    # 8      dist[sorgente] := 0 ;                                        // Distanza dalla sorgente alla sorgente
    # 9      Q := L'insieme di tutti i nodi nel Grafo ;                       // Tutti i nodi nel grafo sono
    # 10                                                                 // Non ottimizzati e quindi stanno in Q
    # 11      while Q  non è  vuota:                                      // Loop principale
    # 12          u := vertice in Q with smallest distance in dist[] ;    // Nodo iniziale per il primo caso
    # 13          rimuovi u da Q ;
    # 14          if dist[u] = infinito:
    # 15              break ;                                            // tutti i vertici rimanenti sono
    # 16          end if                                                 // inaccessibili dal nodo sorgente
    # 17
    # 18          For each neighbor v di u:                              // dove v non è ancora stato
    # 19                                                                 // rimosso da Q.
    # 20              alt := dist[u] + dist_tra(u, v) ;
    # 21              if alt < dist[v]:                                  // Rilascia (u,v,a)
    # 22                  dist[v] := alt ;
    # 23                  precedente[v] := u ;
    # 24                  decrease-key v in Q;                           // Riordina v nella coda
    # 25              end if
    # 26          end for
    # 27      end while
    # 28  return dist;
    # possiamo terminare la ricerca alla riga 13 se u = destinazione

    @staticmethod
    def dijkstra(status, source, target):
        """Search a path from a source to a targer."""
        try:
            from sys import maxint
        except ImportError:
            from sys import maxsize as maxint
        from random import choice
        dist = dict()
        prev = dict()
        for airport in status.airports:
            dist[airport] = maxint
            prev[airport] = None

        dist[source] = 0
        q_nodes = [name for name in status.airports]

        print("SOURCE & TARGET", source, target)

        while len(q_nodes) > 0:
            print("Q_NODES", q_nodes)
            print("WHILE DIST", dist)
            smallest = choice(
                [vert for vert, val in dist.items()
                 if val == min([val_2 for vert_2, val_2 in dist.items() if vert_2 in q_nodes]) and vert in q_nodes])
            print("Smallest", smallest)
            q_nodes.remove(smallest)
            if smallest == target:
                break
            if dist[smallest] == maxint:
                break

            for neighbor, weight in status.airports[smallest].neighbors.items():
                print("FOR:", neighbor, weight)
                alt = dist[smallest] + weight
                print("ALT:", alt)
                if alt < dist[neighbor]:
                    print("IF:", alt, dist[neighbor])
                    dist[neighbor] = alt
                    prev[neighbor] = smallest

        print("DIST", dist)
        print("PREV", prev)

        result = list()
        tmp = target
        result.append(tmp)
        while prev[tmp] is not None:
            result.append(prev[tmp])
            tmp = prev[tmp]
        result = [elem for elem in reversed(result)]
        print("RESULT", result)
        return result

    def solve(self, status, goal):
        anction_list = list()
        places = goal.keys()
        targets = [item for list_ in goal.values() for item in list_]
        print("places:", places)
        print("targets:", targets)
        print("moves", status.moves)
        print("where is? Is in", self.where_is(status, targets[0]))
        self.dijkstra(status,
                      self.where_is(status, targets[0], airport_only=True),
                      self.where_is(status, self.get_target_place(goal, targets[0]), airport_only=True))
        return anction_list
