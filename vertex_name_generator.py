from string import ascii_uppercase


# TODO: Expand the number of possible vertex names. Now only 26 are available.
class VertexNameGenerator:
    __vertex_names = tuple(ascii_uppercase.replace('O', '').replace('Z', ''))
    __counter = 0

    @staticmethod
    def get_vertex_name():
        name = VertexNameGenerator.__vertex_names[VertexNameGenerator.__counter]
        VertexNameGenerator.__counter += 1
        return name
