"""
4. Cree las siguientes clases:
    1. `Head`
    2. `Torso`
    3. `Arm`
    4. `Hand`
    5. `Leg`
    6. `Feet`
    7. Ahora cree una clase de `Human` y conecte todas las clases de manera lógica por medio de atributos.
        1. Por ejemplo (*este código esta incompleto, pero describe la idea*):
        
        class Torso:
            def __init__(self, head, right_arm, ...):
                self.head = head
                self.right_arm = right_arm
                ...

        class Arm:
            def __init__(self, hand):
                self.hand = hand


            right_hand = Hand()
            right_arm = Arm(right_hand)
            torso = Torso(head, right_arm)
"""

def build_main_body_part(_part_side, body_parts):
    body_part = {}
    body_part.update({_part_side: []})
    for _, _body_part in body_parts.get_result().items():
        body_part.update({_part_side: _body_part})
    return body_part

def get_body_part_result(_body_yes, body_side, main_body_parts):
    body_part = {}
    body_part.update({body_side: []})
    if _body_yes is None:
            body_part.update({body_side: "No"})
    else:
        for _part in main_body_parts:
            body_part[body_side].append(_part)
    return body_part


def print_results(human_body):
    print("\nThese are the part of my body: ")
    for human_part in human_body.get_result():
        if isinstance(human_part, str):
            print(f"\n==> {human_part}")
        if isinstance(human_part, dict):
            for kpart, vextension in human_part.items():
                print(f"\n====> {kpart}: ")
                for part in vextension:
                    print(f"======> {part}")
    print("\n")


class Head:
    # ears, eyes, nose, mouth, forhead, cheek, chin and jaw
    def __init__(self):
        self.ears = "ears"
        self.eyes = "eyes"
        self.nose = "nose"
        self.mouth = "mouth"
        self.forhead = "forhead"
        self.cheek = "cheek"
        self.chin = "chin"
        self.jaw = "jaw"
        
    def get_result(self):
        head_list = [self.ears, self.eyes, self.nose, self.mouth,
                     self.forhead, self.cheek, self.chin, self.jaw]
        head = {"head": []}
        for part in head_list:
            head["head"].append(part)
        return head

class Torso:
    # chest, abdomen, pelvis, and back.
    def __init__(self, right_arm=None, left_arm=None,
                 right_leg=None, left_leg=None, head=None):
        self.chest = "chest"
        self.abdomen = "abdomen"
        self.pelvis = "pelvis"
        self.back = "back"
        self.all_body_parts = [head, right_arm, left_arm, right_leg, left_leg]

    def get_result(self):
        torso_list = [self.chest, self.abdomen, self.pelvis, self.back]
        _torso = {"torso": []}
        for part in torso_list:
            _torso["torso"].append(part)
        self.all_body_parts.insert(0, _torso) 
        return self.all_body_parts

class Arm:
    # hand, elbow and shoulder
    def __init__(self, right_left="", no_arm=1):
        self.right_left = right_left
        if no_arm == 0:
            self.arm = None
        else:
            self.hand = "hand"
            self.elbow = "elbow"
            self.shoulder = "shoulder"
            self.arm = no_arm

    def get_result(self, _class=None):
        _arm_side = f"{self.right_left}_arm"
        if self.arm is None:
            return f"No {self.right_left} Arm"
        if self.arm == 1:
            arm = build_main_body_part(_arm_side, _class)
            for body, part in arm.items():
                part.extend([self.hand, self.elbow, self.shoulder])
            arm.update({body: part})
            return arm

class Hand:
    # fingers, nails, palm and wrist
    def __init__(self, right_left="", no_hand=1):
        self.right_left = right_left
        if no_hand == 0:
            self._hand = None
        else:
            self.fingers = "fingers"
            self.nails = "nails"
            self.palm = "palm"
            self.wrist = "wrist"
            self._hand = no_hand
    
    def get_result(self):
        body_list = [self.fingers, self.nails, self.palm, self.wrist]
        hand_part = f"{self.right_left}_hand"
        hand = get_body_part_result(self._hand, hand_part, body_list)
        return hand

class Leg:
    # foot and knees
    def __init__(self, right_left="", no_leg=1):
        self.right_left = right_left
        if no_leg == 0:
            self._leg = None
        else:
            self.foot = "foot"
            self.knees = "knees"
            self._leg = no_leg

    def get_result(self, _class=None):
        _leg_side = f"{self.right_left}_leg"
        _feet_side = f"{self.right_left}_feet"
        if self._leg is None:
            return f"No {self.right_left} Leg"
        if self._leg == 1:
            leg = build_main_body_part(_leg_side, _class)
            for body, part in leg.items():
                part.extend([self.foot, self.knees])
            leg.update({body: part})
            return leg

class Feet:
    # toe, toe nails, ankle, sole and heel
    def __init__(self, right_left="", no_feet=1):
        self.right_left = right_left
        if no_feet == 0:
            self._feet = None
        else:
            self.toe = "toe"
            self.toe_nails = "toe_nails"
            self.ankle = "ankle"
            self.sole = "sole"
            self.heel = "heel"
            self._feet = no_feet
            
    def get_result(self):
        body_list = [self.toe, self.toe_nails, self.ankle, self.sole, self.heel]
        feet_part = f"{self.right_left}_feet"
        feet = get_body_part_result(self._feet, feet_part, body_list)
        return feet

class Human:
    def __init__(self):
        self.right_hand = Hand(right_left="right")
        self.left_hand = Hand(right_left="left")
        self.right_arm = Arm(right_left="right")
        self.left_arm = Arm(right_left="left")
        self.right_feet = Feet(right_left="right")
        self.left_feet = Feet(right_left="left")
        self.right_leg = Leg(right_left="right")
        self.left_leg = Leg(right_left="left")
        self.head = Head()
        
    def get_result(self):
        right_arm = self.right_arm.get_result(_class=self.right_hand)
        left_arm = self.left_arm.get_result(_class=self.left_hand)
        right_leg = self.right_leg.get_result(_class=self.right_feet)
        left_leg = self.left_leg.get_result(_class=self.left_feet)
        head = self.head.get_result()
        _torso = Torso(right_arm, left_arm, right_leg, left_leg, head)
        human_parts = _torso.get_result()
        return human_parts


human_body = Human()
print_results(human_body)
