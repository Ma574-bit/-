from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Equipment, Status, Repair

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    
    return render(request, 'login.html', {'error': error})

def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    error = None
    success = None
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        # ตรวจสอบข้อมูล
        if not username:
            error = 'กรุณาระบุชื่อผู้ใช้'
        elif len(username) < 4:
            error = 'ชื่อผู้ใช้ต้องมีอย่างน้อย 4 ตัวอักษร'
        elif User.objects.filter(username=username).exists():
            error = 'ชื่อผู้ใช้นี้มีอยู่แล้ว'
        elif not email:
            error = 'กรุณาระบุอีเมล'
        elif User.objects.filter(email=email).exists():
            error = 'อีเมลนี้มีอยู่แล้ว'
        elif not password:
            error = 'กรุณาระบุรหัสผ่าน'
        elif len(password) < 6:
            error = 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'
        elif password != password_confirm:
            error = 'รหัสผ่านไม่ตรงกัน'
        else:
            # สร้างบัญชีใหม่
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            success = 'สร้างบัญชีสำเร็จ! กรุณาล็อกอินเข้าสู่ระบบ'
            return redirect('login')
    
    return render(request, 'register.html', {
        'error': error,
        'success': success
    })

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    repairs = Repair.objects.all().order_by('-repair_date')
    return render(request, 'home.html', {
        'repairs': repairs,
        'total_repairs': repairs.count(),
        'pending_repairs': repairs.filter(status__name='รอซ่อม').count(),
        'completed_repairs': repairs.filter(status__name__in=['ซ่อมเสร็จ', 'ซ่อมเสร็จแล้ว']).count(),
    })

@login_required(login_url='login')
def report_repair(request):
    equipments = Equipment.objects.all()

    if request.method == 'POST':
        equipment_id = request.POST.get('equipment')
        detail = request.POST.get('detail')
        other_equipment = request.POST.get('other_equipment', '').strip()
        other_location = request.POST.get('other_location', '').strip()

        if not equipment_id:
            return render(request, 'report.html', {
                'equipments': equipments,
                'error': 'กรุณาเลือกอุปกรณ์'
            })

        # ถ้าเลือก "อื่น ๆ" ให้สร้างอุปกรณ์ใหม่
        if equipment_id == 'other':
            if not other_equipment:
                return render(request, 'report.html', {
                    'equipments': equipments,
                    'error': 'กรุณาระบุชื่ออุปกรณ์'
                })
            if not other_location:
                return render(request, 'report.html', {
                    'equipments': equipments,
                    'error': 'กรุณาระบุสถานที่ตั้ง'
                })
            
            # สร้างอุปกรณ์ใหม่
            equipment, created = Equipment.objects.get_or_create(
                name=other_equipment,
                location=other_location
            )
        else:
            equipment = get_object_or_404(Equipment, id=equipment_id)

        # สร้าง Status ถ้าไม่มี
        status, created = Status.objects.get_or_create(name='รอซ่อม')

        Repair.objects.create(
            equipment=equipment,
            detail=detail,
            status=status,
            user=request.user
        )

        return redirect('home')

    return render(request, 'report.html', {
        'equipments': equipments
    })

@login_required(login_url='login')
def repair_detail(request, repair_id):
    repair = get_object_or_404(Repair, id=repair_id)
    statuses = Status.objects.all()
    
    if request.method == 'POST':
        # quick action: mark as completed
        if 'mark_completed' in request.POST:
            status, created = Status.objects.get_or_create(name='ซ่อมเสร็จแล้ว')
            repair.status = status
            repair.save()
            return redirect('repair_detail', repair_id=repair.id)

        status_id = request.POST.get('status')
        if status_id:
            status = get_object_or_404(Status, id=status_id)
            repair.status = status
            repair.save()
            return redirect('repair_detail', repair_id=repair.id)
    
    return render(request, 'repair_detail.html', {
        'repair': repair,
        'statuses': statuses
    })

@login_required(login_url='login')
def repair_list(request):
    repairs = Repair.objects.all().order_by('-repair_date')
    status_filter = request.GET.get('status')
    
    if status_filter:
        repairs = repairs.filter(status__id=status_filter)
    
    statuses = Status.objects.all()
    
    return render(request, 'repair_list.html', {
        'repairs': repairs,
        'statuses': statuses,
        'selected_status': status_filter
    })
