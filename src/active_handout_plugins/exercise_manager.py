import json


class ExerciseManager:
    def __init__(self, course_slug: str):
        self.__course_slug = course_slug
        self.__exercises = {}

    def extract_tags(self, page_url: str, tag_tree: dict):
        '''Extract tags available in tag_tree from page_url.'''
        available_tags = self.__get_available_tags(tag_tree)
        return [
            part for part in page_url.split('/') if part in available_tags
        ]

    def add_exercise(self, page_url: str, el_id: str, tags: list[str], meta: dict=None):
        '''Adds exercise to manager and returns computed slug.'''
        if meta is None:
            meta = {}

        slash = '' if page_url.endswith('/') else '/'
        slug = f'{page_url}{slash}{el_id}'

        page_exercises = self.__exercises.setdefault(page_url, {})
        page_exercises[el_id] = {
            'tags': tags,
            'slug': slug,
            **meta
        }

        return slug

    def exercise_json(self):
        '''Returns json string with all exercise data.'''
        return json.dumps({
            'course': self.__course_slug,
            'exercises': self.__exercises,
        }, indent=2)

    def __get_available_tags(self, tag_tree: list):
        tags = []
        for tag in tag_tree:
            if isinstance(tag, dict):
                for slug, children in tag.items():
                    tags.append(slug)
                    tags += self.__get_available_tags(children)
            else:
                tags.append(tag)
        return tags
