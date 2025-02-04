#include <stdio.h>
#include <stdlib.h>


typedef struct {
    int jour;
    int mois;
    int annee;
} DateNais;

typedef struct {
    char nom[30];
    char prenom[30];
    DateNais date;
} Ouvrier;
int main() {
    Ouvrier ouv1;

    printf("Entrez le nom de l'ouvrier : ");
    scanf("%s", ouv1.nom);
    printf("Entrez le prénom de l'ouvrier : ");
    scanf("%s", ouv1.prenom);
    printf("Entrez la date de naissance (jour mois année) : ");
    scanf("%d %d %d", &ouv1.date.jour , &ouv1.date.mois , &ouv1.date.annee);

    printf("\nInformations de l'ouvrier :\n");
    printf("Nom : %s\n",ouv1.nom);
    printf("Prenom : %s\n",ouv1.prenom);
    printf("Date de naissance : %02d/%02d/%04d\n",ouv1.date.jour, ouv1.date.mois, ouv1.date.annee);

    return 0;
    
}


