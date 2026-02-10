from memoryeditor import MemoryEditor
import tkinter as tk
import threading
import struct
import time

class HeartsHack:
    def __init__(self, ui):
        self.ui = ui
        self.paths = {
            "card_count": (0x9E150,[0xC0, 0x0, 0x28, 0x130, 0x0]),
            'card_data': (0x9E150,[0xC0, 0x0, 0x28, 0x140, 0x0, 0x8, 0x0]),
            'player': (0x9E150,[0xC0, 0x0, 0x0]),
            'tips': (0x9E150,[0x88, 0x13]),
        }
        
        self.patterns_replace = {
            "free_play": ("75 DB 48 8B D6", "90 90 48 8B D6"),
            "exposed_hand": ("40 8A D5 48 8B 0C 0E","B2 01 90 48 8B 0C 0E")
        }
        self.patterns = {
            "win": "8B C6 4C 8D 9C 24 20 01 00 00 49 8B 5B 20",
            "invincible_1":"0F 87 62 36 02 00",
            "invincible_2":"33 F6 48 8B 80 40 01 00 00",
            "invincible_3":"41 C6 04 24 01 33 DB",
            "exposed_hand": "40 F6 C7 03 0F 84 ?? ?? ?? ?? 48"
        }
        self.editor = MemoryEditor("Hearts.exe")
        self.pm = self.editor.connect()
        self._pre_win()
        self._pre_invincible()
        self._free_play_backend = None
        self._invincible_backend = None
        self._close_tips_backend = None
        self._exposed_hand_backend_1 = None
        self._exposed_hand_backend_2 = None
        self._keep_see_all_thread = None
        self._keep_see_all_stop_event = threading.Event()

    def _pre_win(self):
        self._flag_address = self.pm.allocate(4)
        patch_address = self.editor.search(self.patterns['win'], False, True, True)[0]['address']
        shellcode = bytearray([
            0x8B, 0xC6,                                                         # mov eax,esi
            0x4C, 0x8D, 0x9C, 0x24, 0x20, 0x01, 0x00, 0x00,                     # lea r11, qword ptr ss:[rsp+120]
            0x51,                                                               # push rcx
            0x48, 0xB9,                                                         # mov rcx, imm64
        ])
        shellcode += struct.pack('<Q', self._flag_address)
        shellcode.extend([
            0x80, 0x39, 0x01,                                                   # cmp byte ptr [rcx], 1
            0x75, 0x08,                                                         # jne 8
            0xB8, 0x07, 0x00, 0x00, 0x00,                                       # mov eax, 7
            0xC6, 0x01, 0x00,                                                   # mov byte ptr [rcx], 0
        ])
        jmp_offset_pos = len(shellcode)
        shellcode.extend([
            0x59,                                                               # pop rcx
            0xE9,                                                               # jmp rel32
            0x00, 0x00, 0x00, 0x00,                                             # placeholder
        ])
        shellcode_addr = self.editor.alloc_near(patch_address, len(shellcode))
        jmp_offset = (patch_address + 9) - (shellcode_addr + jmp_offset_pos + 5)
        shellcode[jmp_offset_pos + 2:jmp_offset_pos + 6] = struct.pack('<i', jmp_offset)
        rel32 = shellcode_addr - (patch_address + 5)
        patch_bytes = bytearray([0xE9])
        patch_bytes += struct.pack('<i', rel32)
        patch_bytes.extend([0x90, 0x90, 0x90, 0x90, 0x90])
        self.editor.replace(patch_address, patch_bytes)
        self.editor.write_value(shellcode_addr, shellcode, "bytes")

    def _pre_invincible(self):
        player_addr = self.editor.calculate_pointer_chain(0x9E150,[0xC0, 0x0, 0x0])
        patch_address = self.editor.search(self.patterns['invincible_1'], False, True, True)[0]['address']
        jne_address = self.editor.search(self.patterns['invincible_2'], False, True, True)[0]['address']
        jmp_address = self.editor.search(self.patterns['invincible_3'], False, True, True)[0]['address']
        shellcode = bytearray([
            0x81, 0xFA,                         # cmp edx, imm32
        ])
        shellcode += struct.pack('<I', player_addr)
        jne_offset_pos = len(shellcode)
        shellcode.extend([
            0x0F, 0x85,                         # jne rel32
            0x00, 0x00, 0x00, 0x00,             # placeholder
        ])
        jmp_offset_pos = len(shellcode)
        shellcode.extend([
            0xE9,                               # jmp rel32
            0x00, 0x00, 0x00, 0x00,             # placeholder
        ])
        shellcode_addr = self.editor.alloc_near([patch_address, jne_address, jmp_address], len(shellcode))
        jne_next_instr = shellcode_addr + jne_offset_pos + 6
        jne_offset = jne_address - jne_next_instr
        struct.pack_into('<i', shellcode, jne_offset_pos + 2, jne_offset)
        jmp_next_instr = shellcode_addr + jmp_offset_pos + 5
        jmp_offset = jmp_address - jmp_next_instr
        struct.pack_into('<i', shellcode, jmp_offset_pos + 1, jmp_offset)
        self.editor.write_value(shellcode_addr, shellcode, "bytes")
        rel32 = shellcode_addr - (patch_address + 6)
        patch_bytes = bytearray([0x0F, 0x87])
        patch_bytes += struct.pack('<i', rel32)
        self.patterns_replace['invincible'] = (self.patterns['invincible_1'], patch_bytes)

    def _keep_see_all(self):
        suit_map = {0: "♣梅花", 1:"♦方片", 2:"♠黑桃", 3:"♥红桃"}
        number_map = {11:"J", 12:"Q", 13:"K", 14:"A"}
        player_map = {1:"上家", 2:"对家", 3:"下家"}
        card_count_base_offset, card_count_offsets = self.paths["card_count"]
        card_count_offsets = list(card_count_offsets)
        card_data_base_offset, card_data_offsets = self.paths["card_data"]
        card_data_offsets = list(card_data_offsets)
        while not self._keep_see_all_stop_event.is_set():
            for i in range(1, 4):
                player_name = player_map[i]
                listbox = self.ui.listboxes[player_name]
                self.ui.after(0, listbox.delete, 0, 'end')
                card_count_offsets[1] = i * 0x8
                card_count = self.editor.calculate_pointer_chain(card_count_base_offset, card_count_offsets)
                origin_data = []
                for j in range(card_count):
                    card_data_offsets[1] = i * 0x8
                    card_data_offsets[4] = j * 0x8
                    origin_data.append(self.editor.calculate_pointer_chain(card_data_base_offset, card_data_offsets))
                for j in sorted(origin_data):
                    number = (j % 13) + 2
                    suit = j // 13
                    card_text = f"{suit_map[suit]}{number if number <= 10 else number_map[number]}"
                    color = "red" if suit & 1 else "black"
                    self.ui.after(0, lambda lb=listbox, text=card_text, col=color: 
                        lb.insert(tk.END, text) or lb.itemconfig(tk.END, fg=col))
            time.sleep(1)

    def see_all(self):
        try:
            if not self._keep_see_all_thread:
                self._keep_see_all_stop_event.clear()
                self._keep_see_all_thread = threading.Thread(target=self._keep_see_all, daemon=True)
                self._keep_see_all_thread.start()
                return True
        except:
            return False
        
    def cancel_see_all(self):
        try:
            if self._keep_see_all_thread:
                self._keep_see_all_stop_event.set()
                self.ui.listboxes["上家"].delete(0, 'end')
                self.ui.listboxes["对家"].delete(0, 'end')
                self.ui.listboxes["下家"].delete(0, 'end')
                self._keep_see_all_thread = None
                return True
        except:
            return False
        
    def free_play(self):
        try:
            if not self._free_play_backend:
                self._free_play_backend = self.editor.search_and_replace(*self.patterns_replace['free_play'], replace_all=False, base_only=True)
                tips_address = self.editor.calculate_pointer_chain(*self.paths["tips"])
                if self.editor.read_value(tips_address, "byte") == b'\x01':
                    self._close_tips_backend = True
                    self.editor.write_value(tips_address, [0], "bytes")
            return True
        except:
            return False
        
    def cancel_free_play(self):
        try:
            if self._free_play_backend:
                for i in self._free_play_backend['data']:
                    self.editor.search_and_replace(i['new'], i['original'], replace_all=False, base_only=True)
                self._free_play_backend = None
                if self._close_tips_backend:
                    tips_address = self.editor.calculate_pointer_chain(*self.paths["tips"])
                    self.editor.write_value(tips_address, [1], "bytes")
                return True
        except:
            return False
        
    def win(self):
        try:
            self.editor.write_value(self._flag_address, [1], 'bytes')
            return True
        except:
            return False
    
    def god_mode(self):
        try:
            if not self._invincible_backend:
                self._invincible_backend = self.editor.search_and_replace(*self.patterns_replace['invincible'], replace_all=False, base_only=True)
            return True
        except:
            return False

    def cancel_god_mode(self):
        try:
            if self._invincible_backend:
                for i in self._invincible_backend['data']:
                    self.editor.search_and_replace(i['new'], i['original'], replace_all=False, base_only=True)
                self._invincible_backend = None
            return True
        except:
            return False
        
    def exposed_hand(self):
        try:
            if not self._exposed_hand_backend_1:
                self._exposed_hand_backend_1 = self.editor.search_and_replace(*self.patterns_replace['exposed_hand'], replace_all=False, base_only=True)
                exposed_hand_address = self.editor.search(self.patterns['exposed_hand'], False, True, True)[0]['address']
                self._exposed_hand_backend_2 = self.editor.replace(exposed_hand_address, "40 F6 C7 00")
            return True
        except:
            return False
        
    def cancel_exposed_hand(self):
        try:
            if self._exposed_hand_backend_1:
                for i in self._exposed_hand_backend_1['data']:
                    self.editor.search_and_replace(i['new'], i['original'], replace_all=False, base_only=True)
                self.editor.replace(self._exposed_hand_backend_2['address'], self._exposed_hand_backend_2['original'])
                self._exposed_hand_backend_1 = None
                self._exposed_hand_backend_2 = None
            return True
        except:
            return False
