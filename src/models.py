import json
#学生类
class Students:
    def __init__(self,id,name,score):
        self.id = id
        self.name = name
        self.score = score
    def __str__(self):
        return f"学号：{self.id},姓名：{self.name},成绩：{self.score}"
#教务系统类
class StudentSystem:
    def __init__(self):
        self.students = {}
        self.load_students_data()
    def load_students_data(self):   #加载学生信息
        try:    #文件读取的异常处理
            with open('data/students.json','r',encoding="utf-8")as f:
                students_data = json.load(f)
        except FileNotFoundError:   #找不到文件
            print("错误：找不到数据文件 data/students.json，请检查路径")
            return
        except json.JSONDecodeError as e:   #文件为空或格式错误
            if e.pos == 0:
                print("错误:数据文件是空的(0 字节)，请先填入数据")
            else:
                print(f"错误:JSON 格式错误，第 {e.lineno} 行第 {e.colno} 列：{e.msg}")
            return
        except PermissionError:     #文件被占用
            print("错误：没有权限读取数据文件")
            return
        if not students_data:   #文件为空
            print("提示：数据文件内容为空，暂无学生")
            return
        for student in students_data:
            sid = str(student.get("id") or "").strip() 
            name = str(student.get("name") or "").strip()
            if not sid:
                print("警告：有一条记录缺少学号，已跳过")
                continue
            if not name:
                print(f"警告：学号 {sid} 缺少姓名，已跳过")
                continue
            try:
                score = float(student.get("score"))
            except (TypeError, ValueError):      #清除成绩错误的数据
                print(f"警告：学号 {sid} 的成绩不是数字，已跳过")
                continue
            if not 0 <= score <=100:    
                print(f"警告：学号 {sid} 的成绩 {score:g} 不在0~100之间，已跳过")
                continue
            self.students[sid] = Students(sid,name,score)
        print(f"学生信息加载成功,共 {len(self.students)} 条")
    def max_score(self):    #最高分
        if not self.students:
            print("暂无学生信息")
            return
        max_stu = list(self.students.values())[0]
        for stu in self.students.values():           
            if stu.score > max_stu.score:           
                max_stu = stu                   
        print(f"最高分:{max_stu}") 
    def min_score(self):    #最低分
        if not self.students:
            print("暂无学生信息")
            return
        min_stu = list(self.students.values())[0]
        for stu in self.students.values():
            if stu.score < min_stu.score:
                min_stu = stu
        print(f"最低分:{min_stu}")
    def avg_score(self):    #平均分
        if not self.students:
            print("暂无学生信息")
            return 
        total = 0
        for stu in self.students.values():
            total += stu.score
        print(f"平均分：{total/len(self.students)}") 
    def pass_num(self):     #及格人数
        if not self.students:
            print("暂无学生信息")
            return 
        passnum = 0 
        for stu in self.students.values():
            if stu.score >= 60:
                passnum += 1
        print(f"考试及格人数:{passnum}")
    def search_student(self):   #查询学生
        if not self.students:
            print("暂无学生信息")
            return
        stu_id = input("请输入要查询的学生学号：").strip()
        for stu in self.students.values():
            if stu.id == stu_id:
                print(stu) 
                break
        else:
            print("未查询到该学生，请重新输入") 
    def all_student(self):
        if not self.students:
            print("暂无学生信息")
            return 
        for stu in self.students.values():
            print(stu)
    def run(self):
        print("欢迎使用教务系统~")
        while True:
            print()
            print("1.查询考试平均分2.查询考试最高分和最低分3.查询及格人数4.查询指定学生成绩5.查询所有学生成绩6.退出系统")
            print()
            choice = input("请输入您的操作(1-6):").strip()
            match choice:
                case "1":
                    self.avg_score()
                case "2":
                    if not self.students:
                        print("暂无学生信息")
                    else:
                        self.max_score()
                        self.min_score()
                case "3":
                    self.pass_num()
                case "4":
                    self.search_student()
                case "5":
                    self.all_student()
                case "6":
                    print("本次使用结束")
                    break
                case _:
                    print("输入错误，请重新输入")

