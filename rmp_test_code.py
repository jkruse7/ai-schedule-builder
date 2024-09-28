import ratemyprofessor as rmp


def get_prof_difficulty(prof_list: list) -> list:

    school = rmp.get_school_by_name("University of Pittsburgh")
    difficulty_list = []
    for name in prof_list:
        prof = rmp.get_professor_by_school_and_name(school, name)
        if prof is not None:
            difficulty_list.append(prof.difficulty)
    
    return difficulty_list


if __name__ == '__main__':
    test_list = ['William Garrison', 'Sherif Khattab']
    print(get_prof_difficulty(test_list))