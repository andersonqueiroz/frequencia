$(window).ready(function(){
    setInterval(function(){
        var s = parseInt($(".s").html());
        if(s == 59){
            var m = parseInt($(".m").html());
            if(m != 59){
                if(m < 9){
                    $(".m").html("0"+(m + 1));
                }else{
                    $(".m").html(m + 1);
                }
            }else{
                $(".m").html("00");
                var h = parseInt($(".h").html());
                if(h < 9){
                    $(".h").html("0"+(h + 1));
                }else{
                    $(".h").html(h + 1);
                }
            }
            s = parseInt(-1);
        }
        if(s < 9){
            $(".s").html("0"+(s + 1));
        }else{
            $(".s").html(s + 1);
        }
    },1000);
});
