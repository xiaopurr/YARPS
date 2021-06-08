classdef Swimmer < handle
    properties (Constant)
        sigma = 1;
        ymin = -50;
        dt = 1;
    end
    properties
        x;
        y;
        theta;
        D;
        Dr;
        va;
        vfield;
        vfx;
        vfy;
        traj=[];
        %rOrientation;
        ori=[];
        time= 0;
    end
    methods
        function obj = Swimmer(D, va, vfield)
            obj.x = 0;
            obj.y = 0;
            obj.theta = 0;
            obj.D  = D;
            obj.Dr = D*(3/4)*(1/((obj.sigma/2)^2));
            obj.va = va;
            
            obj.vfield = vfield;
            obj.vfx = vfield(1);
            obj.vfy = vfield(2);
        end
        function onestep(obj)
            %Brownian Motion
            obj.ori=[obj.ori, obj.theta];
            obj.traj=[obj.traj; obj.x, obj.y];
            obj.x = obj.x+(sqrt(2*obj.D/obj.dt)*normrnd(0,1)+obj.vfx)*obj.dt;
            obj.y = obj.y+(sqrt(2*obj.D/obj.dt)*normrnd(0,1)+obj.vfy)*obj.dt;
            %Active Swimming
            obj.theta = obj.theta + sqrt(2*obj.Dr/obj.dt)*normrnd(0,1)*obj.dt;
            obj.x = obj.x+sin(obj.theta)*obj.va*obj.dt;
            obj.y = obj.y+cos(obj.theta)*obj.va*obj.dt;
            %bottom wall
            if obj.y < obj.ymin
                obj.y = obj.ymin;
            end
        end
        function timeE(obj, T_total)
            for i=1:T_total
                onestep(obj);
            end
        end
    end
end
