from math import ceil

from .base_screens import Screens, draw_menu_buttons, cat_profiles, draw_next_prev_cat_buttons

from scripts.utility import draw_large, draw, update_sprite
from scripts.game_structure.buttons import buttons
from scripts.game_structure.text import *
from scripts.cat.cats import Cat

class ChooseMentorScreen(Screens):

    def on_use(self):
        verdana_big.text('Choose Mentor', ('center', 30))
        living_cats = []
        for cat in Cat.all_cats.values():
            if not cat.dead and cat != game.switches[
                    'apprentice'].mentor and cat.status in [
                        'warrior', 'deputy', 'leader'
                    ]:
                living_cats.append(cat)
        all_pages = 1
        if len(living_cats) > 20:
            all_pages = int(ceil(len(living_cats) / 20.0))
        pos_x = 0
        pos_y = 0
        cats_on_page = 0
        for x in range(len(living_cats)):
            if x + (game.switches['list_page'] - 1) * 20 > len(living_cats):
                game.switches['list_page'] = 1
            if game.switches['list_page'] > all_pages:
                game.switches['list_page'] = 1
            the_cat = living_cats[x + (game.switches['list_page'] - 1) * 20]
            if not the_cat.dead:
                buttons.draw_button((130 + pos_x, 180 + pos_y),
                                    image=the_cat.sprite,
                                    cat=the_cat.ID,
                                    cur_screen='choose mentor screen2')

                name_len = verdana.text(str(the_cat.name))
                verdana.text(str(the_cat.name),
                             (130 + pos_x - name_len / 2, 240 + pos_y))
                cats_on_page += 1
                pos_x += 100
                if pos_x >= 600:
                    pos_x = 0
                    pos_y += 100
                if cats_on_page >= 20 or x + (game.switches['list_page'] -
                                              1) * 20 == len(living_cats) - 1:
                    break
        verdana.text(
            'page ' + str(game.switches['list_page']) + ' / ' + str(all_pages),
            ('center', 600))

        if game.switches['list_page'] > 1:
            buttons.draw_button((300, 600),
                                text='<',
                                list_page=game.switches['list_page'] - 1,
                                hotkey=[23])

        if game.switches['list_page'] < all_pages:
            buttons.draw_button((-300, 600),
                                text='>',
                                list_page=game.switches['list_page'] + 1,
                                hotkey=[21])

        draw_menu_buttons()

class ChooseMentorScreen2(Screens):

    def on_use(self):
        # use this variable to point to the cat object in question
        the_cat = Cat.all_cats.get(game.switches['cat'])

        # back and next buttons on the profile page
        previous_cat = 0
        next_cat = 0

        for check_cat in Cat.all_cats:
            if Cat.all_cats[check_cat].ID == the_cat.ID:
                next_cat = 1

            if next_cat == 0 and Cat.all_cats[
                    check_cat].ID != the_cat.ID and not Cat.all_cats[
                        check_cat].dead and Cat.all_cats[
                            check_cat].status in [
                                'warrior', 'deputy', 'leader'
                            ] and Cat.all_cats[check_cat] != game.switches[
                                'apprentice'].mentor and not Cat.all_cats[
                                    check_cat].exiled:
                previous_cat = Cat.all_cats[check_cat].ID
            elif next_cat == 1 and Cat.all_cats[check_cat].ID != the_cat.ID and not Cat.all_cats[check_cat].dead and Cat.all_cats[check_cat].status in ['warrior',
                                                                                                                                                                          'deputy',
                                                                                                                                                                          'leader'] and \
                    Cat.all_cats[check_cat] != game.switches['apprentice'].mentor and not Cat.all_cats[
                    check_cat].exiled:
                next_cat = Cat.all_cats[check_cat].ID
            elif int(next_cat) > 1:
                break

        if next_cat == 1:
            next_cat = 0

        if next_cat != 0:
            buttons.draw_button((-40, 40),
                                text='Next Cat',
                                cat=next_cat,
                                hotkey=[21])
        if previous_cat != 0:
            buttons.draw_button((40, 40),
                                text='Previous Cat',
                                cat=previous_cat,
                                hotkey=[23])

        # Info in string
        cat_name = str(the_cat.name)  # name
        cat_thought = the_cat.thought  # thought

        # LAYOUT
        count = 0
        count2 = 0
        verdana_big.text(cat_name, ('center', 70))  # NAME
        draw_large(the_cat, ('center', 100))  # IMAGE
        verdana_small.text(the_cat.genderalign, (250, 330 + count * 15))
        count += 1  # SEX / GENDER
        verdana_small.text(the_cat.status, (450, 330 + count2 * 15))
        count2 += 1  # STATUS
        if 'apprentice' in the_cat.status:
            if the_cat.mentor is not None:
                verdana_small.text('mentor: ' + str(the_cat.mentor.name),
                                   (450, 330 + count2 * 15))
                count2 += 1
        if len(the_cat.apprentice) != 0:
            if len(the_cat.apprentice) == 1:
                apps = 'apprentice: ' + str(the_cat.apprentice[0].name)
            else:
                apps = 'apprentices: '
                for cat in the_cat.apprentice:
                    apps += str(cat.name) + ', '
                apps = apps[:len(apps) - 2]
            verdana_small.text(apps, (450, 330 + count2 * 15))
            count2 += 1
        if len(the_cat.former_apprentices
               ) != 0 and the_cat.former_apprentices[0] is not None:
            if len(the_cat.former_apprentices) == 1:
                former_apps = 'former apprentice: ' + str(
                    the_cat.former_apprentices[0].name)
            else:
                former_apps = 'former apprentices: '
                for cat in the_cat.former_apprentices:
                    former_apps += str(cat.name) + ', '
                former_apps = former_apps[:len(former_apps) - 2]
            verdana_small.text(former_apps, (450, 330 + count2 * 15))
            count2 += 1
        if the_cat.age == 'kitten':
            verdana_small.text('young', (250, 330 + count * 15))
        elif the_cat.age == 'elder':
            verdana_small.text('senior', (250, 330 + count * 15))
        else:
            verdana_small.text(the_cat.age, (250, 330 + count * 15))
        count += 1  # AGE
        verdana_small.text(the_cat.trait, (450, 330 + count2 * 15))
        count2 += 1  # CHARACTER TRAIT
        verdana_small.text(the_cat.skill, (450, 330 + count2 * 15))
        count2 += 1  # SPECIAL SKILL
        verdana_small.text('eyes: ' + the_cat.eye_colour.lower(),
                           (250, 330 + count * 15))
        count += 1  # EYE COLOR
        verdana_small.text('pelt: ' + the_cat.pelt.name.lower(),
                           (250, 330 + count * 15))
        count += 1  # PELT TYPE
        verdana_small.text('fur length: ' + the_cat.pelt.length,
                           (250, 330 + count * 15))
        count += 1  # PELT LENGTH

        # PARENTS
        if the_cat.parent1 is None:
            verdana_small.text('parents: unknown', (250, 330 + count * 15))
            count += 1
        elif the_cat.parent2 is None:
            par1 = str(the_cat.all_cats[the_cat.parent1].name)
            verdana_small.text('parents: ' + par1 + ', unknown',
                               (250, 330 + count * 15))
            count += 1
        else:
            if the_cat.parent1 in the_cat.all_cats and the_cat.parent2 in the_cat.all_cats:
                par1 = str(the_cat.all_cats[the_cat.parent1].name)
                par2 = str(the_cat.all_cats[the_cat.parent2].name)
            elif the_cat.parent1 in the_cat.all_cats:
                par2 = "Error: Cat#" + the_cat.parent2 + " not found"
                par1 = str(the_cat.all_cats[the_cat.parent1].name)
            elif the_cat.parent2 in the_cat.all_cats:
                par1 = "Error: Cat#" + the_cat.parent1 + " not found"
                par2 = str(the_cat.all_cats[the_cat.parent2].name)
            else:
                par1 = "Error: Cat#" + the_cat.parent1 + " not found"
                par2 = "Error: Cat#" + the_cat.parent2 + " not found"

            verdana_small.text('parents: ' + par1 + ' and ' + par2,
                               (250, 330 + count * 15))
            count += 1

        # MOONS
        if the_cat.dead:
            if the_cat.moons == 1:
                verdana_small.text(
                    str(the_cat.moon) + ' moons (in life)',
                    (250, 330 + count * 15))
                count += 1
            elif the_cat.moons != 1:
                verdana_small.text(
                    str(the_cat.moons) + ' moons (in life)',
                    (250, 330 + count * 15))
                count += 1
            if the_cat.dead_for == 1:
                verdana_small.text(
                    str(the_cat.dead_for) + ' moon (in death)',
                    (250, 330 + count * 15))
                count += 1
            elif the_cat.dead_for != 1:
                verdana_small.text(
                    str(the_cat.dead_for) + ' moons (in death)',
                    (250, 330 + count * 15))
                count += 1
        else:
            if the_cat.moons == 1:
                verdana_small.text(
                    str(the_cat.moons) + ' moon', (250, 330 + count * 15))
                count += 1
            elif the_cat.moons != 1:
                verdana_small.text(
                    str(the_cat.moons) + ' moons', (250, 330 + count * 15))
                count += 1

        # MATE
        if the_cat.mate is not None and not the_cat.dead:
            if the_cat.mate in Cat.all_cats:
                if Cat.all_cats.get(
                        the_cat.mate
                ).dead:  # TODO: fix when mate dies mate becomes none
                    verdana_small.text(
                        'former mate: ' +
                        str(Cat.all_cats[the_cat.mate].name),
                        (250, 330 + count * 15))
                else:
                    verdana_small.text(
                        'mate: ' + str(Cat.all_cats[the_cat.mate].name),
                        (250, 330 + count * 15))
                count += 1
            else:
                verdana_small.text(
                    'Error: mate: ' + str(the_cat.mate) + " not found",
                    ('center', 495))

        # experience
        if not the_cat.dead:
            verdana_small.text('experience: ' + str(the_cat.experience_level),
                               (450, 330 + count2 * 15))
            count2 += 1
        else:
            verdana_small.text('experience: ' + str(the_cat.experience_level),
                               (450, 330 + count2 * 15))
            count2 += 1

        # buttons

        buttons.draw_button(
            ('center', -100),
            text='Choose as ' + str(game.switches['apprentice'].name) +
            '\'s mentor',
            cur_screen=game.switches['last_screen'],
            cat_value=the_cat,
            apprentice=game.switches['apprentice'])
        buttons.draw_button(('center', -50),
                            text='Back',
                            cur_screen='clan screen',
                            hotkey=[0])

class ViewChildrenScreen(Screens):

    def on_use(self):
        the_cat = Cat.all_cats[game.switches['cat']]
        verdana_big.text(f'Family of {str(the_cat.name)}', ('center', 50))
        verdana.text('Parents:', ('center', 85))
        if the_cat.parent1 is None:
            verdana_small.text('Unknown', (342, 165))
        elif the_cat.parent1 in Cat.all_cats:
            buttons.draw_button(
                (350, 120),
                image=Cat.all_cats[the_cat.parent1].sprite,
                cat=the_cat.parent1,
                cur_screen='profile screen')

            name_len = verdana.text(
                str(Cat.all_cats[the_cat.parent1].name))
            verdana_small.text(str(Cat.all_cats[the_cat.parent1].name),
                               (375 - name_len / 2, 185))

        else:
            verdana_small.text(f'Error: cat {str(the_cat.parent1)} not found',
                               (342, 165))
        if the_cat.parent2 is None:
            verdana_small.text('Unknown', (422, 165))
        elif the_cat.parent2 in Cat.all_cats:
            buttons.draw_button(
                (430, 120),
                image=Cat.all_cats[the_cat.parent2].sprite,
                cat=the_cat.parent2,
                cur_screen='profile screen')

            name_len = verdana.text(
                str(Cat.all_cats[the_cat.parent2].name))
            verdana_small.text(str(Cat.all_cats[the_cat.parent2].name),
                               (455 - name_len / 2, 185))

        else:
            verdana_small.text(
                'Error: cat ' + str(the_cat.parent2) + ' not found',
                (342, 165))

        pos_x = 0
        pos_y = 20
        siblings = False
        for x in game.clan.clan_cats:
            if (Cat.all_cats[x].parent1 in (the_cat.parent1, the_cat.parent2) or Cat.all_cats[x].parent2 in (
                    the_cat.parent1, the_cat.parent2) and the_cat.parent2 is not None) and the_cat.ID != Cat.all_cats[x].ID and the_cat.parent1 is not None and \
                    Cat.all_cats[x].parent1 is not None:
                buttons.draw_button((40 + pos_x, 220 + pos_y),
                                    image=Cat.all_cats[x].sprite,
                                    cat=Cat.all_cats[x].ID,
                                    cur_screen='profile screen')

                name_len = verdana.text(str(Cat.all_cats[x].name))
                verdana_small.text(str(Cat.all_cats[x].name),
                                   (65 + pos_x - name_len / 2, 280 + pos_y))

                siblings = True
                pos_x += 80
                if pos_x > 640:
                    pos_y += 70
                    pos_x = 0
        if siblings:
            verdana.text('Siblings:', ('center', 210))
        else:
            verdana.text('This cat has no siblings.', ('center', 210))
        buttons.draw_button(('center', -100),
                            text='Back',
                            cur_screen='profile screen')
        pos_x = 0
        pos_y = 60
        kittens = False
        for x in game.clan.clan_cats:
            if the_cat.ID in [
                    Cat.all_cats[x].parent1,
                    Cat.all_cats[x].parent2
            ]:
                buttons.draw_button((40 + pos_x, 370 + pos_y),
                                    image=Cat.all_cats[x].sprite,
                                    cat=Cat.all_cats[x].ID,
                                    cur_screen='profile screen')

                name_len = verdana.text(str(Cat.all_cats[x].name))
                verdana_small.text(str(Cat.all_cats[x].name),
                                   (65 + pos_x - name_len / 2, 430 + pos_y))

                kittens = True
                pos_x += 80
                if pos_x > 640:
                    pos_y += 70
                    pos_x = 0
        if kittens:
            verdana.text('Offspring:', ('center', 400))
        else:
            verdana.text('This cat has never had offspring.', ('center', 400))
        buttons.draw_button(('center', -100),
                            text='Back',
                            cur_screen='profile screen')

    def screen_switches(self):
        cat_profiles()

class ChooseMateScreen(Screens):

    def on_use(self):
        the_cat = Cat.all_cats[game.switches['cat']]
        verdana_big.text(f'Choose mate for {str(the_cat.name)}',
                         ('center', 50))
        verdana_small.text(
            'If the cat has chosen a mate, they will stay loyal and not have kittens with anyone else,',
            ('center', 80))
        verdana_small.text(
            'even if having kittens in said relationship is impossible.',
            ('center', 95))
        verdana_small.text(
            'Chances of having kittens when possible is heightened though.',
            ('center', 110))

        draw_large(the_cat, (200, 130))
        self._extracted_from_on_use_29(the_cat, 70)
        mate = None
        if game.switches['mate'] is not None and the_cat.mate is None:
            mate = Cat.all_cats[game.switches['mate']]
        elif the_cat.mate is not None:
            if the_cat.mate in Cat.all_cats:
                mate = Cat.all_cats[the_cat.mate]
            else:
                the_cat.mate = None
        if mate is not None:
            draw_large(mate,(450, 130))
            verdana.text(str(mate.name), ('center', 300))
            self._extracted_from_on_use_29(mate, -100)
            if the_cat.gender == mate.gender and not game.settings[
                    'no gendered breeding']:
                verdana_small.text(
                    '(this pair will not be able to have kittens)',
                    ('center', 320))

        valid_mates = []
        pos_x = 0
        pos_y = 20
        if the_cat.mate is None:
            self._extracted_from_on_use_42(the_cat, valid_mates, pos_x, pos_y)
        else:
            verdana.text('Already in a relationship.', ('center', 340))
            kittens = False
            for x in game.clan.clan_cats:
                if the_cat.ID in [
                        Cat.all_cats[x].parent1,
                        Cat.all_cats[x].parent2
                ] and mate.ID in [
                        Cat.all_cats[x].parent1,
                        Cat.all_cats[x].parent2
                ]:
                    buttons.draw_button((200 + pos_x, 370 + pos_y),
                                        image=Cat.all_cats[x].sprite,
                                        cat=Cat.all_cats[x].ID,
                                        cur_screen='profile screen')

                    kittens = True
                    pos_x += 50
                    if pos_x > 400:
                        pos_y += 50
                        pos_x = 0
            if kittens:
                verdana.text('Their offspring:', ('center', 360))
            else:
                verdana.text('This pair has never had offspring.',
                             ('center', 360))
        if mate is not None and the_cat.mate is None:
            buttons.draw_button(('center', -130),
                                text="It\'s official!",
                                cat_value=the_cat,
                                mate=mate)

        elif the_cat.mate is not None:
            buttons.draw_button(('center', -130),
                                text="Break it up...",
                                cat_value=the_cat,
                                mate=None)

        buttons.draw_button(('center', -100),
                            text='Back',
                            cur_screen='profile screen')

    # TODO Rename this here and in `on_use`
    def _extracted_from_on_use_42(self, the_cat, valid_mates, pos_x, pos_y):
        for x in game.clan.clan_cats:
            relevant_cat = Cat.all_cats[x]
            invalid_age = relevant_cat.age not in ['kitten', 'adolescent']

            direct_related = the_cat.is_sibling(relevant_cat) or the_cat.is_parent(relevant_cat) or relevant_cat.is_parent(the_cat)
            indirect_related = the_cat.is_uncle_aunt(relevant_cat) or relevant_cat.is_uncle_aunt(the_cat)
            related = direct_related or indirect_related

            not_aviable = relevant_cat.dead or relevant_cat.exiled

            if not related and relevant_cat.ID != the_cat.ID and invalid_age and not not_aviable and relevant_cat.mate == None:
                valid_mates.append(relevant_cat)
        all_pages = int(ceil(len(valid_mates) /
                             27.0)) if len(valid_mates) > 27 else 1
        cats_on_page = 0
        for x in range(len(valid_mates)):
            if x + (game.switches['list_page'] - 1) * 27 > len(valid_mates):
                game.switches['list_page'] = 1
            if game.switches['list_page'] > all_pages:
                game.switches['list_page'] = 1
            pot_mate = valid_mates[x + (game.switches['list_page'] - 1) * 27]
            buttons.draw_button((100 + pos_x, 320 + pos_y),
                                image=pot_mate.sprite,
                                mate=pot_mate.ID)

            pos_x += 50
            cats_on_page += 1
            if pos_x > 400:
                pos_y += 50
                pos_x = 0
            if cats_on_page >= 27 or x + (game.switches['list_page'] -
                                          1) * 27 == len(valid_mates) - 1:
                break
        verdana.text(
            'page ' + str(game.switches['list_page']) + ' / ' + str(all_pages),
            ('center', 600))

        if game.switches['list_page'] > 1:
            buttons.draw_button((300, 600),
                                text='<',
                                list_page=game.switches['list_page'] - 1,
                                hotkey=[23])

        if game.switches['list_page'] < all_pages:
            buttons.draw_button((-300, 600),
                                text='>',
                                list_page=game.switches['list_page'] + 1,
                                hotkey=[21])

    # TODO Rename this here and in `on_use`
    def _extracted_from_on_use_29(self, arg0, arg1):
        verdana_small.text(arg0.age, (arg1, 200))
        if (arg0.genderalign is not None):
            verdana_small.text(arg0.genderalign, (arg1, 215))
        else:
            verdana_small.text(arg0.gender, (arg1, 215))
        verdana_small.text(arg0.trait, (arg1, 230))

    def screen_switches(self):
        game.switches['mate'] = None
        cat_profiles()

class RelationshipScreen(Screens):
    bool = {True: 'on', False: 'off', None: 'None'}

    def on_use(self):
        # use this variable to point to the cat object in question
        the_cat = Cat.all_cats.get(game.switches['cat'],
                                         game.clan.instructor)

        # back and next buttons on the relationships page
        draw_next_prev_cat_buttons(the_cat)

        # USER INTERFACE ART
        search_text = game.switches['search_text']
        search_bar = pygame.transform.scale(
            pygame.image.load("resources/images/relationship_search.png").convert_alpha(), (228, 39))

        screen.blit(search_bar, (536, 90))
        verdana_black.text(game.switches['search_text'], (612, 97))

        details_frame = pygame.transform.scale(
            pygame.image.load("resources/images/relationship_details_frame.png").convert_alpha(), (254, 344))
        screen.blit(details_frame, (25, 130))

        toggle_frame = pygame.transform.scale(
            pygame.image.load("resources/images/relationship_toggle_frame.png").convert_alpha(), (251, 120))
        screen.blit(toggle_frame, (45, 484))

        list_frame = pygame.transform.scale(
            pygame.image.load("resources/images/relationship_list_frame.png").convert_alpha(), (502, 500))
        screen.blit(list_frame, (273, 122))

        # button for better displaying
        verdana_mid.text(
            f"Show Dead",
            (70, 513))
        if game.settings['show dead relation'] is False:
            buttons.draw_image_button((169, 505),
                                      button_name='on',
                                      size=(46, 34),
                                      text='switch',
                                      setting='show dead relation',
                                      )
            buttons.draw_image_button((215, 505),
                                      button_name='off',
                                      size=(46, 34),
                                      text='switch',
                                      setting='show dead relation',
                                      available=False
                                      )

        if game.settings['show dead relation'] is True:
            buttons.draw_image_button((169, 505),
                                      button_name='on',
                                      size=(46, 34),
                                      text='switch',
                                      setting='show dead relation',
                                      available=False
                                      )
            buttons.draw_image_button((215, 505),
                                      button_name='off',
                                      size=(46, 34),
                                      text='switch',
                                      setting='show dead relation',
                                      )

        verdana_mid.text(
            f"Show Empty",
            (70, 558))
        if game.settings['show empty relation'] is False:
            buttons.draw_image_button((169, 550),
                                      button_name='on',
                                      size=(46, 34),
                                      text='switch',
                                      setting='show empty relation'
                                      )
            buttons.draw_image_button((215, 550),
                                      button_name='off',
                                      size=(46, 34),
                                      text='switch',
                                      setting='show empty relation',
                                      available=False
                                      )

        if game.settings['show empty relation'] is True:
            buttons.draw_image_button((169, 550),
                                      button_name='on',
                                      size=(46, 34),
                                      text='switch',
                                      setting='show empty relation',
                                      available=False
                                      )
            buttons.draw_image_button((215, 550),
                                      button_name='off',
                                      size=(46, 34),
                                      text='switch',
                                      setting='show empty relation',
                                      )



        # make a list of the relationships
        search_relations = []
        if search_text.strip() != '':
            for rel in the_cat.relationships:
                if search_text.lower() in str(rel.cat_to.name).lower():
                    search_relations.append(rel)
        else:
            search_relations = the_cat.relationships.copy()

        # LAYOUT
        verdana_big.text(str(the_cat.name) + ' Relationships', (80, 75))  # NAME
        draw(the_cat, (25, 70))  #SPRITE

        if the_cat is None and the_cat.mate != '':
            mate = Cat.all_cats.get(the_cat.mate)
            if mate is None:
                verdana_small.text(
                    f"{str(the_cat.genderalign)}  - {str(the_cat.age)} - {str(the_cat.trait)} -  mate: {str(mate.name)}",
                    (80, 100))
            else:
                verdana_small.text(
                    f"{str(the_cat.genderalign)}  - {str(the_cat.age)} - {str(the_cat.trait)}",
                    (80, 100))
        else:
            verdana_small.text(
                f"{str(the_cat.genderalign)}  - {str(the_cat.age)} - {str(the_cat.trait)}",
                (80, 100))

        # filter relationships based on the settings #TOGGLE IMAGES NOT DONE YET
        if not game.settings['show dead relation']:
            search_relations = list(
                filter(lambda rel: not rel.cat_to.dead, search_relations))

        if not game.settings['show empty relation']:
            search_relations = list(
                filter(
                    lambda rel: (rel.romantic_love + rel.platonic_like + rel.
                                 dislike + rel.admiration + rel.comfortable +
                                 rel.jealousy + rel.trust) > 0, search_relations))

        # pages
        all_pages = 1  # amount of pages
        if len(search_relations) > 8:
            all_pages = int(ceil(len(search_relations) / 8))

        pos_x = 0
        pos_y = 0
        cats_on_page = 0  # how many are on page already
        for x in range(len(search_relations)):
            if (x +
                    (game.switches['list_page'] - 1) * 8) > len(search_relations):
                game.switches['list_page'] = 1
            if game.switches['list_page'] > all_pages:
                game.switches['list_page'] = 1
            the_relationship = search_relations[x +
                                             (game.switches['list_page'] - 1) *
                                             8]
            update_sprite(the_relationship.cat_to)

            buttons.draw_button((312 + pos_x, 150 + pos_y),
                                image=the_relationship.cat_to.sprite,
                                chosen_cat=the_relationship.cat_to,
                                show_details=True)

            # name length
            verdana_mid.text(str(the_relationship.cat_to.name),
                                (290 + pos_x, 131 + pos_y))

            count = 17
            different_age = the_relationship.cat_to.age != the_relationship.cat_to.age
            adult_ages = ['young adult', 'adult', 'senior adult', 'elder']
            both_adult = the_relationship.cat_to.age in adult_ages and the_relationship.cat_to.age in adult_ages
            check_age = (different_age and both_adult) or both_adult or not different_age

            if the_relationship.romantic_love > 49 and check_age:
                verdana_small_light.text(
                    'romantic love:',
                    (292 + pos_x, 181 + pos_y + count))
            else:
                verdana_small.text(
                    'romantic like:',
                    (292 + pos_x, 181 + pos_y + count))
            count += 20
            current_x = 294 + pos_x
            current_y = 180 + pos_y + count
            if check_age:
                self.draw_bar(the_relationship.romantic_love, current_x, current_y)
            else:
                self.draw_bar(0, current_x, current_y)
            count += 5

            if the_relationship.platonic_like > 49:
                verdana_small_light.text(
                    'platonic love:',
                    (292 + pos_x, 179 + pos_y + count))
            else:
                verdana_small.text(
                    'platonic like:',
                    (292 + pos_x, 179 + pos_y + count))
            count += 20
            current_x = 294 + pos_x
            current_y = 178 + pos_y + count
            self.draw_bar(the_relationship.platonic_like, current_x, current_y)

            count += 5

            if the_relationship.dislike > 49:
                verdana_small_light.text(
                    'hate:',
                    (292 + pos_x, 177 + pos_y + count))
            else:
                verdana_small.text(
                    'dislike:',
                    (292 + pos_x, 177 + pos_y + count))
            count += 20
            current_x = 294 + pos_x
            current_y = 176 + pos_y + count
            self.draw_bar(the_relationship.dislike, current_x, current_y)

            count += 5

            if the_relationship.admiration > 49:
                verdana_small_light.text(
                    'admiration:',
                    (292 + pos_x, 175 + pos_y + count))
            else:
                verdana_small.text(
                    'respect:',
                    (292 + pos_x, 175 + pos_y + count))
            count += 20
            current_x = 294 + pos_x
            current_y = 174 + pos_y + count
            self.draw_bar(the_relationship.admiration, current_x, current_y)

            count += 5

            verdana_small.text(
                'comfortable:',
                (292 + pos_x, 173 + pos_y + count))
            count += 20
            current_x = 294 + pos_x
            current_y = 172 + pos_y + count
            self.draw_bar(the_relationship.comfortable, current_x, current_y)

            count += 5

            verdana_small.text(
                'jealousy:',
                (292 + pos_x, 171 + pos_y + count))
            count += 20
            current_x = 294 + pos_x
            current_y = 170 + pos_y + count
            self.draw_bar(the_relationship.jealousy, current_x, current_y)

            count += 5

            verdana_small.text(
                'trust:',
                (294 + pos_x, 169 + pos_y + count))
            count += 20
            current_x = 294 + pos_x
            current_y = 168 + pos_y + count
            self.draw_bar(the_relationship.trust, current_x, current_y)


            cats_on_page += 1
            pos_x += 122
            if pos_x >= 400:
                pos_x = 0
                pos_y += 55 + count

            if cats_on_page >= 8 or x + (game.switches['list_page'] -
                                          1) * 8 == len(search_relations) - 1:
                break


        # SHOW CAT DETAILS

        if game.switches['show_details'] is True:
            if game.switches['chosen_cat'].dead:
                verdana_big.text(
                    f"{str(game.switches['chosen_cat'].name)} (dead)",
                    (60, 295)
                )
            else:
                verdana_big.text(
                    f"{str(game.switches['chosen_cat'].name)}",
                    (60, 295)
                )
            draw_large(game.switches['chosen_cat'], (75, 145))

            # GENDER
            verdana_small.text(
                f"{str(game.switches['chosen_cat'].genderalign)}",
                (60, 325))

            # AGE
            verdana_small.text(
                f"{str(game.switches['chosen_cat'].moons)} moons",
                (60, 340))

            # MATE
            if game.switches['chosen_cat'].mate is not None and the_cat.ID != game.switches['chosen_cat'].mate:
                verdana_small.text(
                    'has a mate',
                    (160, 325)
                )

            elif the_cat.mate is not None and the_cat.mate != '' and game.switches['chosen_cat'].ID == the_cat.mate:
                verdana_small.text(
                    f"{str(the_cat.name)}'s mate",
                    (160, 325)
                )
            else:
                verdana_small.text(
                    'mate: none',
                    (160, 325)
                )

            # TRAIT
            verdana_small.text(
                f"{str(game.switches['chosen_cat'].trait)}",
                (60, 355))

            # RELATED [[[ someone else pls figure out how to make this show up ]]]
            if game.switches['chosen_cat'].is_uncle_aunt(the_cat) or\
                    the_cat.is_uncle_aunt(game.switches['chosen_cat']):
                verdana_small.text(
                    'related',
                    (60, 355))
            if game.switches['chosen_cat'] in the_cat.siblings or\
                    the_cat in game.switches['chosen_cat'].siblings:
                verdana_small.text(
                    'related',
                    (60, 355))

        # PAGE ARROW BUTTONS
        verdana.text(
            'page ' + str(game.switches['list_page']) + ' / ' + str(all_pages),
            (488, 625))

        if game.switches['list_page'] > 1:
            buttons.draw_image_button((440, 616),
                                      button_name='relationship_list_arrow_l',
                                      list_page=game.switches['list_page'] - 1,
                                      size=(34, 34),
                                      hotkey=[23])
        else:
            buttons.draw_image_button((440, 616),
                                      button_name='relationship_list_arrow_l',
                                      list_page=game.switches['list_page'] - 1,
                                      size=(34, 34),
                                      available=False,
                                      hotkey=[23])

        if game.switches['list_page'] < all_pages:

            buttons.draw_image_button((580, 616),
                                      button_name='relationship_list_arrow_r',
                                      list_page=game.switches['list_page'] + 1,
                                      size=(34, 34),
                                      hotkey=[21])
        else:
            buttons.draw_image_button((580, 616),
                                      button_name='relationship_list_arrow_r',
                                      list_page=game.switches['list_page'] + 1,
                                      size=(34, 34),
                                      available=False,
                                      hotkey=[21])

        if game.switches['chosen_cat'] is not None and not game.switches['chosen_cat'].dead:
            the_relationship.cat_to = game.switches['chosen_cat']
            buttons.draw_image_button((85, 390),
                                      button_name='switch_focus',
                                      size=(136, 30),
                                      cat=the_relationship.cat_to.ID,
                                      cur_screen='relationship screen',
                                      show_details=None,
                                      chosen_cat=None
                                      )
            buttons.draw_image_button((85, 420),
                                      button_name='view_profile',
                                      size=(136, 30),
                                      cat=the_relationship.cat_to.ID,
                                      cur_screen='profile screen',
                                      show_details=None,
                                      chosen_cat=None
                                      )
        elif game.switches['chosen_cat'] is not None and game.switches['chosen_cat'].dead:
            buttons.draw_image_button((85, 390),
                                      button_name='switch_focus',
                                      size=(136, 30),
                                      cat=the_relationship.cat_to.ID,
                                      cur_screen='relationship screen',
                                      show_details=None,
                                      chosen_cat=None,
                                      available=False
                                      )
            buttons.draw_image_button((85, 420),
                                      button_name='view_profile',
                                      size=(136, 30),
                                      cat=the_relationship.cat_to.ID,
                                      cur_screen='profile screen',
                                      show_details=None,
                                      chosen_cat=None
                                      )

        else:
            buttons.draw_image_button((85, 390),
                                      button_name='switch_focus',
                                      size=(136, 30),
                                      cat=the_relationship.cat_to.ID,
                                      cur_screen='relationship screen',
                                      show_details=None,
                                      chosen_cat=None,
                                      available=False
                                      )
            buttons.draw_image_button((85, 420),
                                      button_name='view_profile',
                                      size=(136, 30),
                                      cat=the_relationship.cat_to.ID,
                                      cur_screen='profile screen',
                                      show_details=None,
                                      chosen_cat=None,
                                      available=False
                                      )
        buttons.draw_image_button((25, 645),
                                  button_name='back',
                                  text='Back',
                                  size=(105, 30),
                                  cur_screen='profile screen')




    def draw_bar(self, value, pos_x, pos_y):
        # Loading Bar and variables
        bar_bg = pygame.image.load(
            "resources/images/relations_border.png").convert_alpha()
        original_bar = pygame.image.load(
            "resources/images/relation_bar.png").convert_alpha()

        bg_rect = bar_bg.get_rect(midleft=(pos_x, pos_y))
        screen.blit(bar_bg, bg_rect)
        x_pos = 0
        for i in range(int(value / 10)):
            x_pos = i * 11
            bar_rect = original_bar.get_rect(midleft=(pos_x + x_pos + 2, pos_y))
            bar = pygame.transform.scale(original_bar, (10, 10))
            screen.blit(bar, bar_rect)
        x_pos = 11 * int(value / 10)
        bar_rect = original_bar.get_rect(midleft=(pos_x + x_pos + 2, pos_y))
        bar = pygame.transform.scale(original_bar, (value % 10, 10))
        screen.blit(bar, bar_rect)

    def screen_switches(self):
        cat_profiles()
