# -*- coding: utf-8 -*-
from game.processors import GameProcessor

REPLACE_DICTIONARY = {u'<br/>': "\r\n",
                      u'**Автопереход**': u'<b>Автопереход</b>'}


class GameWorker(GameProcessor):
    @staticmethod
    def replace_forbidden_words(updates):
        """
        :param updates:
        :type updates: list of str
        :return:
        """
        replaced_updates = []
        for update in updates:
            if update:
                for word, replace in REPLACE_DICTIONARY.iteritems():
                    update = update.replace(word, replace)
                replaced_updates.append(update)
        return replaced_updates

    def check_updates(self):
        updates = []
        self.game_page = self.game_driver.get_game_page()

        # Check that user is logged in
        if self.process_user_was_not_logged():
            return

        # If games was not started
        updates += self.process_game_not_started()
        # If game was finished
        updates += self.process_game_finished()
        # If game is started and not finished - should start process tasks
        if not (self.game_driver.not_started(self.game_page) or self.game_driver.is_finished(self.game_page)):
            # If can't get task text we should bypass one iteration
            task_text = self.game_driver.get_task(self.game_page)
            if task_text is None:
                return

            # If new task was received:
            updates += self.process_new_task_received()
            # Process AP time
            updates += self.process_ap_time()
            # Process hints
            updates += self.process_hints()
            # Process hints time
            updates + self.process_hints_time()
            # Process codes left
            updates += self.process_codes_left()
            # Catch task was changed
            updates += self.process_task_was_changed()
            # Codes try limited!!
            updates += self.process_tries_limit()
            # Message from ORGS received:
            updates += self.process_org_message()
        return self.replace_forbidden_words(updates)
