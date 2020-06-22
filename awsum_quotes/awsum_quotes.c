#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAX_QUOTES 8
#define MAX_LEN_TEXT 80
#define MAX_LEN_AUTHOR 30

typedef struct quotation {
	char text[MAX_LEN_TEXT];
	char author[MAX_LEN_AUTHOR];
} Quotation;

typedef struct collection {
	int count;
	Quotation quotes[MAX_QUOTES];
} Collection;


void print_intro(){

	puts("                                                            __                 \n_____ __  _  __________ __  _____        ________ __  _____/  |_  ____   ______\n\\__  \\\\ \\/ \\/ /  ___/  |  \\/     \\      / ____/  |  \\/  _ \\   __\\/ __ \\ /  ___/\n / __ \\\\     /\\___ \\|  |  /  Y Y  \\    < <_|  |  |  (  <_> )  | \\  ___/ \\___ \\ \n(____  /\\/\\_//____  >____/|__|_|  /     \\__   |____/ \\____/|__|  \\___  >____  >\n     \\/           \\/            \\/         |__|                      \\/     \\/ \n");
	puts("Collection of the best quotes from the most important personalities of our time.\nFeel free to contribute to the list if you know some good ones!\n");
}


void add_quote(Collection* c, char* new_text, char* new_author){

	int i_new = c->count;

	// copy with correct length
	strncpy(c->quotes[i_new].text, new_text, MAX_LEN_TEXT);
	c->quotes[i_new].text[MAX_LEN_TEXT - 1] = '\0';
	strncpy(c->quotes[i_new].author, new_author, MAX_LEN_AUTHOR);
	c->quotes[i_new].author[MAX_LEN_AUTHOR - 1] = '\0';

	c->count++;
}


void get_new_quote(Collection* c){

	char new_text[MAX_LEN_TEXT];
	char new_author[MAX_LEN_AUTHOR];

	// zero out stack memory to prevent a leak of libc
	memset(new_text, 0, MAX_LEN_TEXT);
	memset(new_author, 0, MAX_LEN_AUTHOR);

	char confirm_string[4];
	char* newline_ptr = NULL;
	char* s_newline = "\n";

	if (c->count < MAX_QUOTES) {
		// get text
		printf("Text: ");
		read(0, new_text, 0x90);
		newline_ptr = strstr(new_text, s_newline);
		if (newline_ptr)
			*newline_ptr = '\0';

		// ask confirmation
		printf("\nAre you sure that the exact words are \"%s\"? They seem too awsum! [y/n] ", new_text);
		fgets(confirm_string, 3, stdin);
		if (confirm_string[0] != 'y') {
			puts("No bad quotes in this collection\n");
			return;
		}

		// get author
		printf("Author: ");
		read(0, new_author, 0x90);
		newline_ptr = strstr(new_author, s_newline);
		if (newline_ptr)
			*newline_ptr = '\0';

		// add to collection
		add_quote(c, new_text, new_author);
		printf("Added to the collection\n\n");

	} else {
		// collection is full
		puts("You know too many awsum quotes!");
		exit(-1);
	}
}


void print_single_quote(Collection* c){

	char usr_index[4];
	int index;

	puts("Which awsum one?");
	fgets(usr_index, 4, stdin);
	index = atoi(usr_index);

	index--;

	if (index > 0 && index <= c->count) {
		printf("\n%s\n", c->quotes[index].text);
		printf("%s\n\n", c->quotes[index].author);
	}
	else
		puts("Index not awsum\n");
}


void print_all(Collection* c){

	int i = 0;

	while (i < c->count) {
		printf("\n%s\n", c->quotes[i].text);
		printf("%s\n", c->quotes[i].author);
		i++;
	}
	puts("");
}


void populate(Collection* c){

	// default quotes
	add_quote(c, "The cause is hidden; the effect is visible to all.", "Ovid");
	add_quote(c, "Manuscripts don't burn.", "Michail Bulgakov");
	add_quote(c, "To succeed, jump as quickly at opportunities as you do at conclusions.", "Benjamin Franklin");
	add_quote(c, "Don't be yourself, be a pizza. Everyone loves pizza.", "Pewdiepie");
	add_quote(c, "I'll never exploit something just because people like it.", "/bin/sh");
}


void print_menu(){

	puts("Menu:");
	puts("[1] Show all");
	puts("[2] Show a specific quote");
	puts("[3] Add quote");
	puts("[4] Quit");
}


int main() {

	char usr_choice[4];
	int choice_n = 0;

	Collection* c = malloc(sizeof(Collection));

	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	c->count = 0;
	populate(c);
	print_intro();

	while (choice_n != 4){
		print_menu();
		fgets(usr_choice, 4, stdin);
		choice_n = atoi(usr_choice);
		switch(choice_n){
			case 1:
				print_all(c);
				break;
			case 2:
				printf("The collection contains %d quotes. ", c->count);
				print_single_quote(c);
				break;
			case 3:
				get_new_quote(c);
				break;
			case 4:
				return 0;
			default:
				puts("Invalid option");
		}
	}
}