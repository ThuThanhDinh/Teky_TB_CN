-tạo admin
python manage.py createsuperuser
-tạo một model dưới database:
python manage.py migrate 
python manage.py makemigrations 
-tạo app 
python manage.py startapp 
django-admin startproject 
- chạy server
python manage.py runserver        

-tài khoản admin:
username: admin
gmail: admin@gmail.com
pass: 123


- cài sendgrid vào project
pip install sendgrid


- vào web https://sendgrid.com/en-us
+ setup điền thông tin
+ email api => chọn integrate guide => chọn send email và tiếp tục điền thông tin=> xác thực
+ vào lại integrate guide => chọn send SMTP Relay
+ nhập vào pass => copy phần pass sau khi mã hóa (api key)
+ vào setting điền thông tin vào:
EMAIL_HOST_PASSWORD = 'your_sendgrid_api_key'
DEFAULT_FROM_EMAIL = 'youremail@gmail.com' (email mà đã xác thực với sendgrid)
+ chạy lại server
+ sau đó vào lại sendgrid tick update to setting=> nhấn verify
+ thử nghiệm
đăng kí một tk sau đó bấm quên mật khẩu
điền email vào 
quay lại sendgrid nhấn integrate

+kiểm tra email (trong spam)


+ làm phần hiển thị bài đăng cho trang web
+ Thêm xóa sửa bài đăng
+ thêm comment cho mỗi bài đăng
+ chỉnh css lại cho hoàn thiện web 

-tạo model cho comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body
    def get_absolute_url(self):
        return reverse('post_list')

-tạo view cho new
class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_new.html'
    fields = ['title', 'body']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'body']
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/comment_new.html'
    fields = ['body']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})
-urls news
    path('post/<int:pk>/',BlogDetailView.as_view(),name ='post_detail'),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_new'),


