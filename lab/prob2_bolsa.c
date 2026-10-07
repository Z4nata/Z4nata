#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef struct cel {
    int senha;
    int valor;
} Pessoa;

Pessoa fila[1000000];


/* Retorna 1 se 'a' deve ficar acima de 'b' no heap:
   maior valor primeiro; em caso de empate, menor senha (chegou antes). */
int temPrioridade(Pessoa a, Pessoa b){
    if (a.valor != b.valor)
        return a.valor > b.valor;
    return a.senha < b.senha;
}

void trocar(int x, int y){
    Pessoa temp = fila[x];
    fila[x] = fila[y];
    fila[y] = temp;
}


/* Insere na posicao 'cont' (primeira livre) e sobe ate a posicao correta. */
void adicionaraoVetor(int val, int i, int cont){
    fila[cont].senha = i;
    fila[cont].valor = val;

    int pos = cont;
    while (pos > 0 && temPrioridade(fila[pos], fila[(pos - 1) / 2])){
        trocar(pos, (pos - 1) / 2);
        pos = (pos - 1) / 2;
    }
}


/* Remove a raiz (maior oferta). 'cont' e o tamanho do heap ja decrementado,
   ou seja, fila[cont] e o ultimo elemento. */
int removerRaiz(int cont){
    int temp = fila[0].senha;

    fila[0] = fila[cont];

    //reorganizar heap (descer)
    int pos = 0;
    while (1){
        int esq = 2 * pos + 1;
        int dir = 2 * pos + 2;
        int maior = pos;

        if (esq < cont && temPrioridade(fila[esq], fila[maior]))
            maior = esq;
        if (dir < cont && temPrioridade(fila[dir], fila[maior]))
            maior = dir;

        if (maior == pos)
            break;

        trocar(pos, maior);
        pos = maior;
    }

    return temp;
}


int main(){

    int i = 1;
    int val;
    char oper[8];
    int cont = 0;

    while(scanf("%7s",oper)!=EOF){
        if(strcmp(oper,"c")==0){

            if (scanf("%d",&val) != 1) break;
            adicionaraoVetor(val, i, cont);
            i++;
            cont++;
        }
        else if(strcmp(oper,"v")==0){

            if( cont > 0){

            cont--;
            printf("%d\n", removerRaiz(cont));

            } else printf("0\n");

        }
        else if(strcmp(oper,"f")==0){
            break;
        }

    }
    return 0;
}
