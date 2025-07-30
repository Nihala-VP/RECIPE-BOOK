from django.shortcuts import render,redirect

from django.views.generic import View

from MyRecipes_App.forms import RegistrationForm,SignInForm,RecipeForm

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.models import User

from MyRecipes_App.models import Recipe

from django.utils.decorators import method_decorator

from MyRecipes_App.decorators import signin_required

# Create your views here.



class SignUpView(View):

    template_name="signup.html"

    form_class=RegistrationForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("signin")
        

        else:

            return render(request,self.template_name,{"form":form_instance})

class SignInView(View):

    template_name="login.html"

    form_class=SignInForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            validated_data=form_instance.cleaned_data

            u_name=validated_data.get("username")

            pwd=validated_data.get("password")

            user_object=authenticate(request,username=u_name,password=pwd)

            if user_object:

              login(request,user_object)

              return redirect("recipe-create")
        
        return render(request,self.template_name,{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
class RecipeCreateView(View):

    template_name="recipe_create.html"

    form_class=RecipeForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
        
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():
          
          validated_data=form_instance.cleaned_data

          Recipe.objects.create(**validated_data,owner=request.user)

          return redirect("recipe-list")
            
        else:

          return render(request,self.template_name,{"form":form_instance})
        
@method_decorator(signin_required,name="dispatch")
class RecipeListView(View):

    template_name="recipe_list.html"


    def get(self,request,*args,**kwargs):

        qs=Recipe.objects.all()

        return render(request,self.template_name,{"data":qs})
    

@method_decorator(signin_required,name="dispatch")
class RecipeDeleteView(View):

    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")

        Recipe.objects.get(id=id).delete()

        return redirect("recipe-list")

@method_decorator(signin_required,name="dispatch")    
class RecipeUpdateView(View):

    template_name="recipe_update.html"

    form_class=RecipeForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        recipe_object=Recipe.objects.get(id=id)

        form_instance=self.form_class(instance=recipe_object)

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        
        id=kwargs.get("pk")

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            validated_data=form_instance.cleaned_data

            Recipe.objects.filter(id=id).update(**validated_data)

            return redirect("recipe-list")
        
        else:

            return render(request,self.template_name,{"form":form_instance})
        
@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")


            

    


        

